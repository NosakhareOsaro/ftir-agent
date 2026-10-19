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


def test_question_file_is_well_formed():
    rows = [json.loads(l) for l in (ROOT / "eval" / "questions.jsonl").read_text().splitlines()]
    assert len(rows) == 25
    assert len({r["id"] for r in rows}) == 25
    for r in rows:
        assert {"id", "category", "question", "reference_answer", "must_mention", "key_pmids"} <= r.keys()
