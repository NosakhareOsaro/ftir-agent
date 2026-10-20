import json
from pathlib import Path

from eval.run_eval import apply_group_rule, citation_spans, keyword_score, sentences_citing

ROOT = Path(__file__).parent.parent


def test_keyword_score():
    groups = [["brummer", "bmm"], ["obes"]]
    assert keyword_score("Loss of bmm causes obesity", groups) == 1.0
    assert keyword_score("Brummer is a lipase", groups) == 0.5
    assert keyword_score("anything", []) is None


def test_sentences_citing():
    ans = "First claim [PMID:11111111]. Second claim [PMID:20202020].\nReferences\n- Smith 2020 [PMID:11111111]"
    assert sentences_citing(ans, "20202020") == ["Second claim [PMID:20202020]."]
    assert sentences_citing(ans, "11111111") == ["First claim [PMID:11111111]."]


def test_citation_after_full_stop_covers_paragraph():
    ans = ("About half are infected. Effects are rarely significant. [PMID:24714809] [PMID:27035832]\n\n"
           "### References\n- Huang W, 2014. Natural variation. [PMID:24714809]")
    assert sentences_citing(ans, "24714809") == [
        "About half are infected. Effects are rarely significant. [PMID:24714809] [PMID:27035832]"]


def test_citation_covers_preceding_uncited_sentences():
    # Audit item #7: the 50% claim had no citation of its own and went unchecked in v1.
    ans = ("Ablated flies survive starvation about 50% longer. The authors suggest slower "
           "mobilisation [PMID:15374818].\n\nReferences\n- Isabel G, 2005.")
    assert sentences_citing(ans, "15374818") == [
        "Ablated flies survive starvation about 50% longer. The authors suggest slower "
        "mobilisation [PMID:15374818]."]


def test_citation_spans_group_co_cited_papers():
    ans = "Uncited intro.\nA is true [PMID:11111111] [PMID:22222222]. B is true [PMID:33333333]."
    assert citation_spans(ans) == [
        ("A is true [PMID:11111111] [PMID:22222222].", ["11111111", "22222222"]),
        ("B is true [PMID:33333333].", ["33333333"])]


def test_group_rule_applied_in_code():
    judged = {"passages": [
        {"passage": 1, "group_verdict": "SUPPORTED", "reason": "",
         "papers": [{"pmid": "11111111", "contributes": True},
                    {"pmid": "22222222", "contributes": True}]},
        {"passage": 2, "group_verdict": "PARTIAL", "reason": "",
         "papers": [{"pmid": "33333333", "contributes": True},
                    {"pmid": 44444444, "contributes": False}]},
    ]}
    got = {(v["passage"], v["pmid"]): v["verdict"] for v in apply_group_rule(judged)}
    assert got == {(1, "11111111"): "SUPPORTED", (1, "22222222"): "SUPPORTED",
                   (2, "33333333"): "PARTIAL", (2, "44444444"): "UNSUPPORTED"}


def test_reference_list_used_only_as_fallback():
    ans = "Body text without citations.\n\nReferences\n- Mackay TF, 2012. The DGRP [PMID:22318601]"
    assert sentences_citing(ans, "22318601") == ["- Mackay TF, 2012. The DGRP [PMID:22318601]"]


def test_question_file_is_well_formed():
    rows = [json.loads(l) for l in (ROOT / "eval" / "questions.jsonl").read_text().splitlines()]
    assert len(rows) == 25
    assert len({r["id"] for r in rows}) == 25
    for r in rows:
        assert {"id", "category", "question", "reference_answer", "must_mention", "key_pmids"} <= r.keys()
