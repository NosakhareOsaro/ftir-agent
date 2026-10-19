"""
tools.py

The four tools the agent can call, their JSON schemas, and the dispatcher.

Every tool returns a JSON-serialisable dict. Errors are returned as
{"error": "..."} rather than raised, so the model can read them and recover
(e.g. retry a search with different terms).
"""

import json

import pandas as pd

from agent import ncbi
from model import ftir

MAX_ABSTRACT_CHARS = 2500


class ToolBox:
    """
    Holds per-session state: the spectra datasets the user has loaded and
    every PMID whose abstract was actually fetched (used for citation checks).
    """

    def __init__(self, datasets=None, model_bundle=None):
        self.datasets = dict(datasets or {})   # name -> (labels, spectra DataFrame)
        self._bundle = model_bundle
        self.fetched = {}                      # pmid -> record from fetch_abstracts

    # ── Tool implementations ─────────────────────────────────────────────────

    def search_pubmed(self, query, max_results=8):
        max_results = max(1, min(int(max_results), 20))
        total, pmids = ncbi.esearch_pubmed(query, max_results)
        summaries = ncbi.esummary_pubmed(pmids)
        return {
            "query": query,
            "total_hits": total,
            "results": [summaries[p] for p in pmids if p in summaries],
            "note": "Titles only. Call fetch_abstracts before citing any of these.",
        }

    def fetch_abstracts(self, pmids):
        pmids = tuple(str(p).strip().removeprefix("PMID:").strip() for p in pmids)[:10]
        records = ncbi.efetch_abstracts(pmids)
        out = []
        for p in pmids:
            rec = records.get(p)
            if rec is None:
                out.append({"pmid": p, "error": "not found in PubMed"})
                continue
            self.fetched[p] = rec
            rec = dict(rec)
            if len(rec["abstract"]) > MAX_ABSTRACT_CHARS:
                rec["abstract"] = rec["abstract"][:MAX_ABSTRACT_CHARS] + " […]"
            if not rec["abstract"]:
                rec["abstract"] = "(no abstract available; do not cite for specific findings)"
            out.append(rec)
        return {"articles": out}

    def lookup_taxon(self, name):
        rec = ncbi.lookup_taxonomy(name)
        if rec is None:
            return {"name": name, "error": "no NCBI Taxonomy match"}
        return rec

    def predict_starvation_resistance(self, dataset):
        if dataset not in self.datasets:
            return {"error": f"unknown dataset '{dataset}'",
                    "available_datasets": list(self.datasets)}
        labels, spectra = self.datasets[dataset]
        bundle = self.bundle
        return {
            "dataset": dataset,
            "model_card": ftir.model_card(bundle),
            "predictions": ftir.predict(bundle, spectra, labels),
        }

    # ── Plumbing ─────────────────────────────────────────────────────────────

    @property
    def bundle(self):
        if self._bundle is None:
            self._bundle = ftir.load_model()
        return self._bundle

    def add_dataset(self, name, df):
        """Validate a user table and register it; raises ftir.SpectrumError."""
        self.datasets[name] = ftir.parse_spectra(df)

    def add_csv(self, name, path):
        self.add_dataset(name, pd.read_csv(path))

    def schemas(self):
        """Tool definitions in OpenAI function-calling format."""
        tools = [
            _fn("search_pubmed",
                "Search PubMed. Returns PMIDs with titles, journals and years "
                "(no abstracts). Use specific scientific terms; try a few phrasings "
                "if the first search is poor.",
                {"query": {"type": "string", "description": "PubMed query"},
                 "max_results": {"type": "integer", "description": "1-20, default 8"}},
                ["query"]),
            _fn("fetch_abstracts",
                "Fetch titles and abstracts for up to 10 PMIDs. You may only cite "
                "papers whose abstracts you fetched with this tool.",
                {"pmids": {"type": "array", "items": {"type": "string"}}},
                ["pmids"]),
            _fn("lookup_taxon",
                "Look up an organism in NCBI Taxonomy: taxid, rank, full lineage, "
                "common name. Use to verify species names.",
                {"name": {"type": "string", "description": "scientific or common name"}},
                ["name"]),
        ]
        if self.datasets:
            tools.append(_fn(
                "predict_starvation_resistance",
                "Run the trained elastic-net model (from the author's MSc dissertation) "
                "on a loaded FTIR spectra dataset. Returns predicted starvation "
                "resistance per spectrum, contributions per spectral band, warnings, "
                "and a model card with limitations.",
                {"dataset": {"type": "string", "enum": list(self.datasets)}},
                ["dataset"]))
        return tools

    def call(self, name, arguments):
        """Run a tool by name with a JSON-string or dict of arguments."""
        fn = {
            "search_pubmed": self.search_pubmed,
            "fetch_abstracts": self.fetch_abstracts,
            "lookup_taxon": self.lookup_taxon,
            "predict_starvation_resistance": self.predict_starvation_resistance,
        }.get(name)
        if fn is None:
            return {"error": f"unknown tool '{name}'"}
        try:
            args = json.loads(arguments) if isinstance(arguments, str) else dict(arguments or {})
            return fn(**args)
        except Exception as exc:  # report to the model, don't crash the loop
            return {"error": f"{type(exc).__name__}: {exc}"}


def _fn(name, description, properties, required):
    return {"type": "function", "function": {
        "name": name, "description": description,
        "parameters": {"type": "object", "properties": properties, "required": required},
    }}
