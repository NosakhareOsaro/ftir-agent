"""
run_eval.py

Run the agent over eval/questions.jsonl and score it.

Metrics
-------
Automatic (no LLM involved):
  citation_exists    cited PMID is a real PubMed record (esummary lookup)
  citation_grounded  cited PMID's abstract was fetched during that run
  key_paper_hit      a known key paper was retrieved (fetched) during the run
  keyword_score      fraction of required facts ("must_mention" groups) present

LLM judge (separate model call; temperature from LLM_TEMPERATURE if set):
  citation_support   for each citation: does the fetched abstract support the
                     sentence that cites it? SUPPORTED / PARTIAL / UNSUPPORTED
  accuracy           answer vs reference answer: 2 correct, 1 partial, 0 wrong

The judge is itself an LLM and can be wrong; see README for the hand audit.

Free-tier friendly: every question's run and judgement is cached as JSON
under eval/runs/<model>/, so an interrupted run resumes where it stopped.

Usage:
  .venv/bin/python eval/run_eval.py                 # run + judge + write results.md
  .venv/bin/python eval/run_eval.py --only lit01 tax04
  .venv/bin/python eval/run_eval.py --no-judge      # automatic metrics only
  .venv/bin/python eval/run_eval.py --report-only   # rebuild results.md from cache
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from agent import ncbi  # noqa: E402
from agent.llm import ChatClient  # noqa: E402
from agent.loop import extract_pmids, run_agent  # noqa: E402
from agent.tools import ToolBox  # noqa: E402

EVAL_DIR = ROOT / "eval"
EXAMPLES = ROOT / "model" / "examples"
DATASET_FILES = {
    "most_resistant": "most_resistant_line_mean.csv",
    "least_resistant": "least_resistant_line_mean.csv",
    "single_flies": "single_flies_mid_line.csv",
}


# ── Scoring helpers ───────────────────────────────────────────────────────────

def keyword_score(answer, groups):
    if not groups:
        return None
    text = answer.lower()
    hits = sum(any(term.lower() in text for term in group) for group in groups)
    return hits / len(groups)


def citation_spans(answer):
    """
    Split the answer into (passage, [cited PMIDs]) pairs.

    A citation covers its own sentence plus any uncited sentences just before
    it in the same paragraph ("Survival rose 50%. The authors suggest X
    [PMID:1]." cites PMID 1 for both). A bare citation after the full stop
    with nothing uncited before it covers the previous sentence. Reference-list
    lines are used only for papers the body never cites.
    """
    parts = re.split(r"^#*\s*References\b.*$", answer, maxsplit=1, flags=re.M | re.I)
    body, refs = parts[0], (parts[1] if len(parts) > 1 else "")
    spans = []
    for para in body.split("\n"):
        sents = [s for s in re.split(r"(?<=[.!?])\s+", para.strip()) if s]
        pending = []
        for i, s in enumerate(sents):
            pmids = extract_pmids(s)
            if not pmids:
                pending.append(s)
                continue
            citation_only = not re.sub(r"[\[\]\s,;]|PMID:?\s*\d+", "", s, flags=re.I)
            if citation_only and not pending and i > 0:
                pending = [sents[i - 1]]
            spans.append((" ".join(pending + [s]), pmids))
            pending = []
    in_body = {p for _, pmids in spans for p in pmids}
    for line in refs.split("\n"):
        pmids = [p for p in extract_pmids(line) if p not in in_body]
        if pmids:
            spans.append((line.strip(), pmids))
    return spans


def sentences_citing(answer, pmid):
    """Every passage in the answer that cites this PMID."""
    return [text for text, pmids in citation_spans(answer) if pmid in pmids] or [answer[:500]]


# v1: one paper per item, only the sentence holding the citation.
# v2: whole cited passage, co-cited abstracts together, grouped-citation rule in
#     the prompt. The judge ignored the rule, so:
# v3: the judge answers two simpler questions per passage (does the group support
#     it all? does each paper support some of it?) and code applies the rule.
JUDGE_VERSION = 3

JUDGE_SUPPORT = """You check citations in a scientific answer.
Each PASSAGE below is followed by the abstracts of every paper it cites.
For each passage, answer two separate questions.

1. group_verdict: taking ALL of the passage's cited abstracts together, is the whole passage
   supported?
   SUPPORTED = every claim in the passage is stated or directly implied by at least one abstract.
   PARTIAL = some claims are supported, but at least one is not, or is overstated.
   UNSUPPORTED = the abstracts do not support the passage.
2. For each cited paper on its own: does its abstract support at least one claim in the
   passage? (true/false). A paper does not need to support the whole passage.

Judge only against the abstracts shown, not outside knowledge.
A reference-list line that only gives author/year/title is SUPPORTED if the title matches.
Reply with JSON only:
{{"passages": [{{"passage": <n>, "group_verdict": "...", "reason": "<25 words",
  "papers": [{{"pmid": "...", "contributes": true}}]}}]}}

{items}"""


def apply_group_rule(judged):
    """
    Turn per-passage answers into one verdict per paper per passage.

    Grouped-citation rule: a paper that supports part of the passage takes the
    group's verdict; a paper that supports none of it is UNSUPPORTED.
    """
    out = []
    for p in judged.get("passages", []):
        for paper in p.get("papers", []):
            verdict = p["group_verdict"] if paper.get("contributes") else "UNSUPPORTED"
            out.append({"passage": p["passage"], "pmid": str(paper["pmid"]),
                        "verdict": verdict, "reason": p.get("reason", "")})
    return out

JUDGE_ACCURACY = """You grade an AI research assistant's answer against a reference answer.
Score 2 if it is correct and covers the key points of the reference.
Score 1 if it is partly correct or misses important points.
Score 0 if it is wrong, fabricates sources or findings, or does not answer.
For questions with a false premise or that the tool cannot answer, the reference
says what a good answer does; score 2 only if the answer does that.
Judge content only, not style or length.
Reply with JSON only: {{"score": 0|1|2, "reason": "<25 words"}}

QUESTION: {question}
REFERENCE ANSWER: {reference}
ASSISTANT ANSWER: {answer}"""


def judge_json(judge, prompt):
    msg = judge.chat([{"role": "user", "content": prompt}])
    text = msg.get("content") or ""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"judge returned no JSON: {text[:200]}")
    return json.loads(match.group(0))


def judge_run(judge, q, run, accuracy=None):
    """Judge citation support and answer accuracy. Pass `accuracy` to reuse a cached score."""
    out = {"judge_version": JUDGE_VERSION, "support": []}
    abstracts = run["abstracts"]
    spans = [(text, [p for p in pmids if p in abstracts])
             for text, pmids in citation_spans(run["answer"])]
    spans = [(text, pmids) for text, pmids in spans if pmids]
    if spans:
        items = "\n\n".join(
            f"PASSAGE {n}: {text}\n" + "\n".join(
                f"  PMID {p}: {abstracts[p]['title']}. {abstracts[p]['abstract'][:2500]}"
                for p in pmids)
            for n, (text, pmids) in enumerate(spans, 1)
        )
        out["raw_support"] = judge_json(judge, JUDGE_SUPPORT.format(items=items))
        out["support"] = apply_group_rule(out["raw_support"])
    out["accuracy"] = accuracy or judge_json(judge, JUDGE_ACCURACY.format(
        question=q["question"], reference=q["reference_answer"], answer=run["answer"]))
    return out


# ── Running ───────────────────────────────────────────────────────────────────

def make_toolbox(q):
    tb = ToolBox()
    for name in q.get("datasets", []):
        path = EXAMPLES / DATASET_FILES[name]
        if not path.exists():
            return None
        tb.add_csv(name, path)
    return tb


def run_one(q, llm):
    tb = make_toolbox(q)
    if tb is None:
        return {"skipped": "example spectra not available (run scripts/train_model.py)"}
    t0 = time.time()
    res = run_agent(q["question"], llm, tb)
    run = res.to_dict()
    run["seconds"] = round(time.time() - t0, 1)
    run["abstracts"] = {p: {"title": r["title"], "abstract": r["abstract"]}
                        for p, r in tb.fetched.items()}
    run["existing_pmids"] = sorted(ncbi.esummary_pubmed(tuple(res.cited_pmids)))
    return run


def load_json(path):
    return json.loads(path.read_text()) if path.exists() else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="question ids to run")
    ap.add_argument("--no-judge", action="store_true")
    ap.add_argument("--report-only", action="store_true")
    ap.add_argument("--rerun", action="store_true", help="ignore cached runs")
    args = ap.parse_args()

    questions = [json.loads(l) for l in (EVAL_DIR / "questions.jsonl").read_text().splitlines() if l]
    if args.only:
        questions = [q for q in questions if q["id"] in args.only]

    llm = None if args.report_only else ChatClient()
    model_name = llm.model if llm else (os.getenv("LLM_MODEL") or _latest_run_dir())
    run_dir = EVAL_DIR / "runs" / re.sub(r"[^\w.-]", "_", model_name)
    run_dir.mkdir(parents=True, exist_ok=True)

    judge = None
    if not (args.report_only or args.no_judge):
        judge = ChatClient(model=os.getenv("JUDGE_MODEL") or llm.model)

    for i, q in enumerate(questions, 1):
        run_path, judge_path = run_dir / f"{q['id']}.json", run_dir / f"{q['id']}.judge.json"
        run = None if args.rerun else load_json(run_path)
        if run is None and llm:
            print(f"[{i}/{len(questions)}] {q['id']}: running agent…", flush=True)
            try:
                run = run_one(q, llm)
            except Exception as exc:
                print(f"   failed: {exc}")
                if str(exc)[:3] in ("401", "402", "403"):
                    sys.exit("Stopping: auth/billing error, retrying other questions won't help.")
                continue
            run_path.write_text(json.dumps(run, indent=1, ensure_ascii=False))
            judge_path.unlink(missing_ok=True)
        if run is None or "skipped" in run:
            continue
        old = load_json(judge_path)
        if judge and (old is None or old.get("judge_version", 1) != JUDGE_VERSION):
            print(f"[{i}/{len(questions)}] {q['id']}: judging…", flush=True)
            accuracy = None
            if old:
                # Keep the older judge's verdicts for comparison and reuse its
                # accuracy score, so only the citation check changes.
                old_path = run_dir / f"{q['id']}.judge-v{old.get('judge_version', 1)}.json"
                old_path.write_text(json.dumps(old, indent=1))
                accuracy = old.get("accuracy")
            try:
                judge_path.write_text(json.dumps(judge_run(judge, q, run, accuracy), indent=1))
            except Exception as exc:
                print(f"   judge failed: {exc}")
                if str(exc)[:3] in ("401", "402", "403"):
                    sys.exit("Stopping: auth/billing error, retrying other questions won't help.")

    all_qs = [json.loads(l) for l in (EVAL_DIR / "questions.jsonl").read_text().splitlines() if l]
    report = build_report(all_qs, run_dir, model_name, judge.model if judge else os.getenv("JUDGE_MODEL"))
    (EVAL_DIR / "results.md").write_text(report)
    print("\n" + report)


def _latest_run_dir():
    dirs = sorted((EVAL_DIR / "runs").glob("*"), key=lambda p: p.stat().st_mtime)
    if not dirs:
        sys.exit("no cached runs yet")
    return dirs[-1].name


# ── Report ────────────────────────────────────────────────────────────────────

def pct(num, den):
    return f"{100 * num / den:.0f}% ({num}/{den})" if den else "n/a"


def build_report(questions, run_dir, model_name, judge_model):
    rows, agg = [], {}
    for q in questions:
        run = load_json(run_dir / f"{q['id']}.json")
        if run is None or "skipped" in run:
            continue
        jd = load_json(run_dir / f"{q['id']}.judge.json") or {}
        cited = run["cited_pmids"]
        # One verdict per cited paper; if the judge repeats one, keep the strictest.
        rank = {"SUPPORTED": 0, "PARTIAL": 1, "UNSUPPORTED": 2}
        verdicts = {}
        for v in jd.get("support", []):
            if v["pmid"] in cited and rank.get(v["verdict"], 2) >= rank.get(verdicts.get(v["pmid"]), -1):
                verdicts[v["pmid"]] = v["verdict"]
        jd["support"] = [{"pmid": p, "verdict": v} for p, v in verdicts.items()]
        r = {
            "id": q["id"], "category": q["category"],
            "cited": len(cited),
            "exists": sum(p in run["existing_pmids"] for p in cited),
            "grounded": sum(p in run["fetched_pmids"] for p in cited),
            "key_hit": (any(p in run["fetched_pmids"] for p in q["key_pmids"])
                        if q["key_pmids"] else None),
            "kw": keyword_score(run["answer"], q["must_mention"]),
            "supported": sum(v["verdict"] == "SUPPORTED" for v in jd.get("support", [])),
            "judged_cites": len(jd.get("support", [])),
            "acc": jd.get("accuracy", {}).get("score"),
            "acc_reason": jd.get("accuracy", {}).get("reason", ""),
            "tools": len(run["trace"]), "llm_requests": run["llm_requests"],
        }
        rows.append(r)
        for key in ("all", q["category"]):
            agg.setdefault(key, []).append(r)

    def summarise(rs):
        cited = sum(r["cited"] for r in rs)
        kh = [r["key_hit"] for r in rs if r["key_hit"] is not None]
        kw = [r["kw"] for r in rs if r["kw"] is not None]
        acc = [r["acc"] for r in rs if r["acc"] is not None]
        return [
            str(len(rs)),
            pct(sum(r["exists"] for r in rs), cited),
            pct(sum(r["grounded"] for r in rs), cited),
            pct(sum(r["supported"] for r in rs), sum(r["judged_cites"] for r in rs)),
            pct(sum(kh), len(kh)),
            f"{100 * sum(kw) / len(kw):.0f}%" if kw else "n/a",
            pct(sum(a == 2 for a in acc), len(acc)),
            f"{sum(acc) / (2 * len(acc)):.2f}" if acc else "n/a",
        ]

    lines = [
        "# Evaluation results", "",
        f"- Agent model: `{model_name}`",
        f"- Judge model: `{judge_model or 'none (automatic metrics only)'}`",
        f"- Questions scored: {len(rows)} of {len(questions)}",
        f"- Generated: {time.strftime('%Y-%m-%d')}", "",
        "| Slice | n | Citations exist | Citations grounded | Citations supported (judge) "
        "| Key paper retrieved | Required facts | Fully correct (judge) | Mean accuracy (0-1) |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for key in ["all"] + sorted(k for k in agg if k != "all"):
        lines.append(f"| {key} | " + " | ".join(summarise(agg[key])) + " |")
    lines += [
        "", "## Per question", "",
        "| id | cited | exist | grounded | supported | key paper | facts | accuracy | judge reason |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        kh = "" if r["key_hit"] is None else ("yes" if r["key_hit"] else "no")
        kw = "" if r["kw"] is None else f"{r['kw']:.0%}"
        acc = "" if r["acc"] is None else r["acc"]
        sup = f"{r['supported']}/{r['judged_cites']}" if r["judged_cites"] else ""
        lines.append(f"| {r['id']} | {r['cited']} | {r['exists']} | {r['grounded']} | {sup} "
                     f"| {kh} | {kw} | {acc} | {r['acc_reason']} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
