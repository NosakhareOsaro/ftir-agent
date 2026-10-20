"""
compare_judges.py

Score each version of the citation judge against the reference labels in
eval/reference_verdicts.json (human spot-check and second reviewer).

Usage: .venv/bin/python eval/compare_judges.py [model-run-dir-name]
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
RANK = {"SUPPORTED": 0, "PARTIAL": 1, "UNSUPPORTED": 2}


def verdicts(run_dir, suffix):
    """{question/PMID: verdict}, strictest verdict when a paper is judged more than once."""
    out = {}
    for path in sorted(run_dir.glob(f"*.{suffix}.json")):
        qid = path.name.split(".")[0]
        for v in json.loads(path.read_text())["support"]:
            key, verdict = f"{qid}/{v['pmid']}", v["verdict"]
            if RANK.get(verdict, 2) >= RANK.get(out.get(key), -1):
                out[key] = verdict
    return out


def main():
    run_dir = ROOT / "eval" / "runs" / (sys.argv[1] if len(sys.argv) > 1 else "gpt-6-luna")
    ref = json.loads((ROOT / "eval" / "reference_verdicts.json").read_text())
    versions = {"v1": verdicts(run_dir, "judge-v1"), "v2": verdicts(run_dir, "judge-v2"),
                "current": verdicts(run_dir, "judge")}

    print(f"| Judge | vs human (n={len(ref['human'])}) | vs second reviewer "
          f"(n={len(ref['second_reviewer'])}) | Supported |")
    print("|---|---|---|---|")
    for name, got in versions.items():
        if not got:
            continue
        cells = []
        for labels in (ref["human"], ref["second_reviewer"]):
            agree = sum(got.get(k) == v for k, v in labels.items())
            cells.append(f"{agree}/{len(labels)}")
        supported = sum(v == "SUPPORTED" for v in got.values())
        print(f"| {name} | {cells[0]} | {cells[1]} | {supported}/{len(got)} |")

    print("\nDisagreements with the reference labels (current judge):")
    for source in ("human", "second_reviewer"):
        for key, want in ref[source].items():
            got = versions["current"].get(key)
            if got != want:
                print(f"  {source:<15} {key:<18} reference {want:<11} judge {got}")


if __name__ == "__main__":
    main()
