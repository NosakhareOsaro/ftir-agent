"""CLI: .venv/bin/python -m agent "your question" [--spectra file.csv ...]"""

import argparse
import json
from pathlib import Path

from agent.llm import ChatClient
from agent.loop import run_agent
from agent.tools import ToolBox


def main():
    ap = argparse.ArgumentParser(description="Ask the FTIR research agent a question.")
    ap.add_argument("question")
    ap.add_argument("--spectra", nargs="*", default=[], help="CSV files of FTIR spectra")
    ap.add_argument("--json", action="store_true", help="print the full result as JSON")
    args = ap.parse_args()

    tb = ToolBox()
    for path in args.spectra:
        tb.add_csv(Path(path).stem, path)

    def show(kind, payload):
        if kind == "tool_call":
            print(f"  → {payload['name']}({payload['arguments']})")

    res = run_agent(args.question, ChatClient(), tb, on_event=show)
    if args.json:
        print(json.dumps(res.to_dict(), indent=2))
        return
    print("\n" + res.answer)
    if res.ungrounded_citations:
        print(f"\n⚠ Cited but never fetched: {', '.join(res.ungrounded_citations)}")


if __name__ == "__main__":
    main()
