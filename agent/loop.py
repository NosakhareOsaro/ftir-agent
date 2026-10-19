"""
loop.py

The agent loop, written by hand (no framework):

  1. Send the system prompt, the question and the tool schemas to the LLM.
  2. If it replies with tool calls, run each one, append the results as
     "tool" messages, and go back to 1.
  3. If it replies with plain text, that is the answer.
  4. After MAX_STEPS rounds of tool calls, ask for an answer without tools.

Then every [PMID:...] in the answer is checked against the abstracts that
were actually fetched in this run.
"""

import json
import re
from dataclasses import dataclass, field

from agent.prompts import FINAL_ANSWER_NUDGE, SYSTEM_PROMPT

MAX_STEPS = 8
MAX_TOOL_RESULT_CHARS = 12000
PMID_RE = re.compile(r"PMID:?\s*(\d{4,9})", re.IGNORECASE)


@dataclass
class AgentResult:
    question: str
    answer: str
    trace: list = field(default_factory=list)   # one entry per tool call
    cited_pmids: list = field(default_factory=list)
    fetched_pmids: list = field(default_factory=list)
    llm_requests: int = 0
    hit_step_limit: bool = False

    @property
    def ungrounded_citations(self):
        """Cited PMIDs whose abstract was never fetched in this run."""
        return [p for p in self.cited_pmids if p not in self.fetched_pmids]

    def to_dict(self):
        return {
            "question": self.question, "answer": self.answer, "trace": self.trace,
            "cited_pmids": self.cited_pmids, "fetched_pmids": self.fetched_pmids,
            "ungrounded_citations": self.ungrounded_citations,
            "llm_requests": self.llm_requests, "hit_step_limit": self.hit_step_limit,
        }


def extract_pmids(text):
    """Unique PMIDs in order of first appearance."""
    return list(dict.fromkeys(PMID_RE.findall(text or "")))


def run_agent(question, llm, toolbox, max_steps=MAX_STEPS, on_event=None):
    """Answer one question. on_event(kind, payload) is called for live UIs."""
    emit = on_event or (lambda kind, payload: None)
    toolbox.fetched.clear()  # citations are checked per question
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": _with_datasets(question, toolbox)},
    ]
    result = AgentResult(question=question, answer="")
    start_requests = llm.n_requests

    for _ in range(max_steps):
        msg = llm.chat(messages, tools=toolbox.schemas())
        # Keep the assistant message exactly as returned: some providers
        # (Gemini 3) attach signatures to tool calls that must be echoed back.
        messages.append(msg)
        calls = msg.get("tool_calls") or []
        if not calls:
            result.answer = msg.get("content") or ""
            break

        for call in calls:
            name = call["function"]["name"]
            args = call["function"].get("arguments") or "{}"
            emit("tool_call", {"name": name, "arguments": args})
            output = toolbox.call(name, args)
            emit("tool_result", {"name": name, "output": output})
            result.trace.append({"tool": name, "arguments": args,
                                 "error": output.get("error") if isinstance(output, dict) else None})
            content = json.dumps(output, ensure_ascii=False, default=str)
            if len(content) > MAX_TOOL_RESULT_CHARS:
                content = content[:MAX_TOOL_RESULT_CHARS] + "…(truncated)"
            messages.append({"role": "tool", "tool_call_id": call.get("id", name),
                             "name": name, "content": content})
    else:
        result.hit_step_limit = True
        messages.append({"role": "user", "content": FINAL_ANSWER_NUDGE})
        result.answer = llm.chat(messages).get("content") or ""

    result.cited_pmids = extract_pmids(result.answer)
    result.fetched_pmids = list(toolbox.fetched)
    result.llm_requests = llm.n_requests - start_requests
    emit("answer", result)
    return result


def _with_datasets(question, toolbox):
    if not toolbox.datasets:
        return question
    names = ", ".join(f"'{n}' ({len(toolbox.datasets[n][0])} spectra)" for n in toolbox.datasets)
    return f"{question}\n\n[Loaded FTIR datasets: {names}]"
