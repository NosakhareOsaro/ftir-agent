"""
make_audit.py

Write eval/judge_audit.md: every citation verdict the LLM judge gave, with
the claim and the abstract, so a human can mark agree/disagree. The
agreement rate goes in the README next to the judge's numbers.

Usage: .venv/bin/python eval/make_audit.py [model-run-dir-name]
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from eval.run_eval import sentences_citing  # noqa: E402

run_dir = ROOT / "eval" / "runs" / (sys.argv[1] if len(sys.argv) > 1 else "gpt-6-luna")
lines = [
    "# Judge audit: citation support", "",
    "For each item, read the claim and the abstract, then replace `?` with "
    "**agree** or **disagree** (with the judge's verdict).", "",
]
n = 0
for judge_path in sorted(run_dir.glob("*.judge.json")):
    qid = judge_path.name.split(".")[0]
    run = json.loads((run_dir / f"{qid}.json").read_text())
    seen = set()
    for v in json.loads(judge_path.read_text())["support"]:
        pmid = v["pmid"]
        if pmid in seen or pmid not in run["abstracts"]:
            continue
        seen.add(pmid)
        n += 1
        abstract = run["abstracts"][pmid]
        lines += [
            f"## {n}. {qid}, PMID {pmid}", "",
            "**Claim:** " + " / ".join(sentences_citing(run["answer"], pmid)), "",
            f"**Abstract:** *{abstract['title']}* {abstract['abstract']}", "",
            f"**Judge:** {v['verdict']}: {v.get('reason', '')}", "",
            "**Your call:** ?", "", "---", "",
        ]
out = ROOT / "eval" / "judge_audit.md"
out.write_text("\n".join(lines))
print(f"{n} verdicts written to {out.relative_to(ROOT)}")
