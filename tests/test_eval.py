import json
from pathlib import Path

from eval.run_eval import keyword_score, sentences_citing

ROOT = Path(__file__).parent.parent


def test_keyword_score():
    groups = [["brummer", "bmm"], ["obes"]]
    assert keyword_score("Loss of bmm causes obesity", groups) == 1.0
    assert keyword_score("Brummer is a lipase", groups) == 0.5
    assert keyword_score("anything", []) is None


def test_sentences_citing():
    ans = "First claim [PMID:1]. Second claim [PMID:2].\nReferences\n- Smith 2020 [PMID:1]"
    assert sentences_citing(ans, "2") == ["Second claim [PMID:2]."]
    assert sentences_citing(ans, "1") == ["First claim [PMID:1]."]


def test_citation_after_full_stop_covers_paragraph():
    ans = ("About half are infected. Effects are rarely significant. [PMID:24714809] [PMID:2]\n\n"
           "### References\n- Huang W, 2014. Natural variation. [PMID:24714809]")
    assert sentences_citing(ans, "24714809") == [
        "About half are infected. Effects are rarely significant. [PMID:24714809] [PMID:2]"]


def test_reference_list_used_only_as_fallback():
    ans = "Body text without citations.\n\nReferences\n- Mackay TF, 2012. The DGRP [PMID:22318601]"
    assert sentences_citing(ans, "22318601") == ["- Mackay TF, 2012. The DGRP [PMID:22318601]"]


def test_question_file_is_well_formed():
    rows = [json.loads(l) for l in (ROOT / "eval" / "questions.jsonl").read_text().splitlines()]
    assert len(rows) == 25
    assert len({r["id"] for r in rows}) == 25
    for r in rows:
        assert {"id", "category", "question", "reference_answer", "must_mention", "key_pmids"} <= r.keys()
