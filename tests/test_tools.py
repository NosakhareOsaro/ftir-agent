from unittest.mock import patch

from agent.tools import ToolBox

ABSTRACT = {"pmid": "123", "title": "T", "journal": "J", "year": "2020", "doi": "", "abstract": "A" * 5000}


def test_fetch_records_pmids_and_truncates():
    tb = ToolBox()
    with patch("agent.ncbi.efetch_abstracts", return_value={"123": ABSTRACT}):
        out = tb.fetch_abstracts(["PMID:123", "999"])
    assert "123" in tb.fetched and "999" not in tb.fetched
    assert out["articles"][0]["abstract"].endswith("[…]")
    assert out["articles"][1]["error"] == "not found in PubMed"


def test_errors_are_returned_not_raised():
    tb = ToolBox()
    assert "error" in tb.call("nope", "{}")
    assert "error" in tb.call("search_pubmed", "not json")
    with patch("agent.ncbi.esearch_pubmed", side_effect=ConnectionError("down")):
        assert "ConnectionError" in tb.call("search_pubmed", {"query": "x"})["error"]


def test_predict_tool_only_offered_with_data(bundle, spectra):
    tb = ToolBox(model_bundle=bundle)
    assert "predict_starvation_resistance" not in [t["function"]["name"] for t in tb.schemas()]
    tb.add_dataset("mine", spectra.iloc[:2])
    names = [t["function"]["name"] for t in tb.schemas()]
    assert "predict_starvation_resistance" in names
    out = tb.call("predict_starvation_resistance", '{"dataset": "mine"}')
    assert len(out["predictions"]) == 2 and "model_card" in out
    assert "available_datasets" in tb.call("predict_starvation_resistance", {"dataset": "x"})
