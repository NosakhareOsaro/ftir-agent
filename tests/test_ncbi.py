from unittest.mock import MagicMock, patch

import pytest

from agent import ncbi
from conftest import network_enabled

EFETCH_XML = """<?xml version="1.0"?><PubmedArticleSet><PubmedArticle>
<MedlineCitation><PMID>42</PMID><Article><Journal><JournalIssue><PubDate><Year>2019</Year></PubDate>
</JournalIssue><Title>Some Journal</Title></Journal><ArticleTitle>A <i>fly</i> paper</ArticleTitle>
<Abstract><AbstractText Label="BACKGROUND">Bg.</AbstractText><AbstractText Label="RESULTS">Res.</AbstractText></Abstract>
</Article></MedlineCitation><PubmedData><ArticleIdList><ArticleId IdType="doi">10.1/x</ArticleId></ArticleIdList></PubmedData>
</PubmedArticle></PubmedArticleSet>"""


def test_efetch_parses_structured_abstract():
    ncbi.efetch_abstracts.cache_clear()
    resp = MagicMock(text=EFETCH_XML)
    with patch("agent.ncbi._get", return_value=resp):
        rec = ncbi.efetch_abstracts(("42",))["42"]
    assert rec["title"] == "A fly paper"
    assert rec["abstract"] == "BACKGROUND: Bg.\nRESULTS: Res."
    assert rec["year"] == "2019" and rec["doi"] == "10.1/x"


@pytest.mark.skipif(not network_enabled(), reason="set RUN_NETWORK_TESTS=1")
def test_live_pubmed_and_taxonomy():
    _, ids = ncbi.esearch_pubmed("Drosophila melanogaster Genetic Reference Panel Mackay 2012", 5)
    assert "22318601" in ids
    assert ncbi.esummary_pubmed(("22318601", "1"))["22318601"]["year"] == "2012"
    assert ncbi.lookup_taxonomy("Drosophila melanogaster")["taxid"] == "7227"
