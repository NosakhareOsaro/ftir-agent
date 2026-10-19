"""
ncbi.py

Thin client for NCBI E-utilities (PubMed + Taxonomy). Free, no key needed.

NCBI asks for at most 3 requests/second without an API key (10 with one),
plus a `tool` and `email` parameter so they can contact you about misuse.
Both are read from the environment:

  NCBI_API_KEY   optional, raises the rate limit to 10 req/s
  NCBI_EMAIL     optional, sent with every request as NCBI asks
"""

import os
import threading
import time
import xml.etree.ElementTree as ET
from functools import lru_cache

import requests

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
TIMEOUT = 20
MAX_RETRIES = 4

_lock = threading.Lock()
_last_call = 0.0


def _min_interval():
    return 0.11 if os.getenv("NCBI_API_KEY") else 0.34


def _get(endpoint, **params):
    """GET an E-utilities endpoint with rate limiting and retry on 429/5xx."""
    global _last_call
    params["tool"] = "ftir-agent"
    if os.getenv("NCBI_EMAIL"):
        params["email"] = os.getenv("NCBI_EMAIL")
    if os.getenv("NCBI_API_KEY"):
        params["api_key"] = os.getenv("NCBI_API_KEY")

    for attempt in range(MAX_RETRIES):
        with _lock:
            wait = _last_call + _min_interval() - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            _last_call = time.monotonic()
        resp = requests.get(f"{EUTILS}/{endpoint}", params=params, timeout=TIMEOUT)
        if resp.status_code == 429 or resp.status_code >= 500:
            time.sleep(2 ** attempt)
            continue
        resp.raise_for_status()
        return resp
    resp.raise_for_status()
    return resp


# ── PubMed ────────────────────────────────────────────────────────────────────

@lru_cache(maxsize=512)
def esearch_pubmed(query, max_results=8):
    """Return (total_hits, [pmid, ...]) for a PubMed query, best match first."""
    data = _get(
        "esearch.fcgi", db="pubmed", term=query, retmax=max_results,
        retmode="json", sort="relevance",
    ).json()["esearchresult"]
    return int(data.get("count", 0)), tuple(data.get("idlist", []))


@lru_cache(maxsize=512)
def esummary_pubmed(pmids):
    """Short records (title, journal, year) for a tuple of PMIDs.

    PMIDs that PubMed does not know are simply absent from the result,
    which is what the citation checker relies on.
    """
    if not pmids:
        return {}
    data = _get("esummary.fcgi", db="pubmed", id=",".join(pmids), retmode="json").json()
    result = data.get("result", {})
    out = {}
    for pmid in result.get("uids", []):
        rec = result[pmid]
        if "error" in rec:
            continue
        out[pmid] = {
            "pmid": pmid,
            "title": rec.get("title", ""),
            "journal": rec.get("source", ""),
            "year": rec.get("pubdate", "")[:4],
            "first_author": (rec.get("authors") or [{}])[0].get("name", ""),
        }
    return out


def _text(el):
    return "".join(el.itertext()).strip() if el is not None else ""


@lru_cache(maxsize=512)
def efetch_abstracts(pmids):
    """Full title + abstract for a tuple of PMIDs, keyed by PMID."""
    if not pmids:
        return {}
    xml = _get("efetch.fcgi", db="pubmed", id=",".join(pmids), retmode="xml").text
    root = ET.fromstring(xml)
    out = {}
    for art in root.iter("PubmedArticle"):
        pmid = _text(art.find(".//MedlineCitation/PMID"))
        sections = []
        for ab in art.findall(".//Abstract/AbstractText"):
            label = ab.get("Label")
            sections.append(f"{label}: {_text(ab)}" if label else _text(ab))
        doi = ""
        for aid in art.findall(".//ArticleIdList/ArticleId"):
            if aid.get("IdType") == "doi":
                doi = _text(aid)
        out[pmid] = {
            "pmid": pmid,
            "title": _text(art.find(".//ArticleTitle")),
            "journal": _text(art.find(".//Journal/Title")),
            "year": _text(art.find(".//JournalIssue/PubDate/Year"))
                    or _text(art.find(".//JournalIssue/PubDate/MedlineDate"))[:4],
            "doi": doi,
            "abstract": "\n".join(sections),
        }
    return out


# ── Taxonomy ──────────────────────────────────────────────────────────────────

@lru_cache(maxsize=256)
def lookup_taxonomy(name):
    """Resolve a taxon name (scientific or common) to its NCBI record, or None."""
    count, ids = _search_taxonomy(name)
    if not ids:
        return None
    xml = _get("efetch.fcgi", db="taxonomy", id=ids[0], retmode="xml").text
    taxon = ET.fromstring(xml).find("Taxon")
    if taxon is None:
        return None
    other = taxon.find("OtherNames")
    common = ""
    if other is not None:
        common = _text(other.find("GenbankCommonName")) or _text(other.find("CommonName"))
    rec = {
        "taxid": _text(taxon.find("TaxId")),
        "scientific_name": _text(taxon.find("ScientificName")),
        "common_name": common,
        "rank": _text(taxon.find("Rank")),
        "lineage": _text(taxon.find("Lineage")),
    }
    if count > 1:
        rec["note"] = (f"{count} taxa matched '{name}'; this is only the first. "
                       "Common names are ambiguous: query the scientific name.")
    return rec


def _search_taxonomy(name):
    data = _get("esearch.fcgi", db="taxonomy", term=name, retmode="json").json()["esearchresult"]
    return int(data.get("count", 0)), tuple(data.get("idlist", []))
