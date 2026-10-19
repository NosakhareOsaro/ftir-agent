import json
from unittest.mock import patch

from agent.loop import extract_pmids, run_agent
from agent.tools import ToolBox
from conftest import FakeLLM, tool_call

REC = {"pmid": "22318601", "title": "The DGRP", "journal": "Nature", "year": "2012", "doi": "", "abstract": "..."}


def test_extract_pmids():
    assert extract_pmids("a [PMID:123456] b [PMID: 123456] c PMID 7654321") == ["123456", "7654321"]


def test_tool_call_then_answer():
    llm = FakeLLM([
        tool_call("fetch_abstracts", json.dumps({"pmids": ["22318601"]})),
        {"role": "assistant", "content": "DGRP lines are inbred [PMID:22318601]. Also [PMID:11111111]."},
    ])
    with patch("agent.ncbi.efetch_abstracts", return_value={"22318601": REC}):
        res = run_agent("What is the DGRP?", llm, ToolBox())
    assert res.cited_pmids == ["22318601", "11111111"]
    assert res.ungrounded_citations == ["11111111"]
    assert res.trace[0]["tool"] == "fetch_abstracts"
    # second request carries the tool result back, matched by id
    tool_msg = llm.sent[1]["messages"][-1]
    assert tool_msg["role"] == "tool" and tool_msg["tool_call_id"] == "call_1"
    assert res.llm_requests == 2


def test_assistant_message_echoed_verbatim():
    """Provider-specific fields (e.g. Gemini thought signatures) must survive."""
    call = tool_call("lookup_taxon", '{"name": "x"}')
    call["tool_calls"][0]["extra_content"] = {"google": {"thought_signature": "sig"}}
    llm = FakeLLM([call, {"role": "assistant", "content": "done"}])
    with patch("agent.ncbi.lookup_taxonomy", return_value=None):
        run_agent("q", llm, ToolBox())
    assert llm.sent[1]["messages"][2]["tool_calls"][0]["extra_content"]["google"]["thought_signature"] == "sig"


def test_step_limit_forces_answer():
    replies = [tool_call("lookup_taxon", '{"name": "x"}') for _ in range(3)]
    llm = FakeLLM(replies + [{"role": "assistant", "content": "best effort"}])
    with patch("agent.ncbi.lookup_taxonomy", return_value=None):
        res = run_agent("q", llm, ToolBox(), max_steps=3)
    assert res.hit_step_limit and res.answer == "best effort"
    assert llm.sent[-1]["tools"] is None
