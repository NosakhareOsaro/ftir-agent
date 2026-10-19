"""Streamlit demo: .venv/bin/streamlit run app.py"""

from pathlib import Path

import pandas as pd
import streamlit as st

from agent.llm import ChatClient, LLMError
from agent.loop import run_agent
from agent.tools import ToolBox
from model import ftir

EXAMPLES = Path(__file__).parent / "model" / "examples"

st.set_page_config(page_title="FTIR Research Agent", page_icon="🪰")
st.title("FTIR Research Agent")
st.caption("Answers Drosophila stress-physiology and spectroscopy questions from real "
           "PubMed abstracts, and runs a trained FTIR → starvation-resistance model.")

if "toolbox" not in st.session_state:
    st.session_state.toolbox = ToolBox()
    st.session_state.history = []
tb = st.session_state.toolbox

# ── Sidebar: model + data ─────────────────────────────────────────────────────
with st.sidebar:
    st.header("Spectra")
    try:
        card = ftir.model_card(tb.bundle)
        st.success(f"Model loaded: elastic net, {card['n_nonzero_coefficients']} "
                   f"wavenumbers, LOO-CV R² = {card['cv_r2_reported']}")
    except FileNotFoundError:
        st.warning("No trained model found. Literature tools still work. "
                   "See README to train the model.")

    upload = st.file_uploader("Upload FTIR spectra (CSV)", type="csv")
    if upload is not None and Path(upload.name).stem not in tb.datasets:
        try:
            tb.add_dataset(Path(upload.name).stem, pd.read_csv(upload))
        except ftir.SpectrumError as exc:
            st.error(f"Could not use {upload.name}: {exc}")
    for csv in sorted(EXAMPLES.glob("*.csv")):
        if csv.stem not in tb.datasets and st.button(f"Load example: {csv.stem}"):
            tb.add_csv(csv.stem, csv)
            st.rerun()
    for name, (labels, _) in tb.datasets.items():
        st.write(f"• **{name}**: {len(labels)} spectra")

    try:
        llm = ChatClient()
        st.caption(f"LLM: `{llm.model}`")
    except LLMError as exc:
        llm = None
        st.error(str(exc))

# ── Chat ──────────────────────────────────────────────────────────────────────
for q, res in st.session_state.history:
    st.chat_message("user").write(q)
    st.chat_message("assistant").markdown(res.answer)

examples = [
    "Which metabolic reserves explain evolved starvation resistance in Drosophila?",
    "Do mid-infrared spectroscopy models of mosquito age transfer to new populations?",
    "What is the NCBI taxid of Drosophila simulans?",
]
question = st.chat_input("Ask a research question…")
if not st.session_state.history and not question:
    st.write("Try:")
    for ex in examples:
        if st.button(ex):
            question = ex

if question and llm:
    st.chat_message("user").write(question)
    with st.chat_message("assistant"):
        status = st.status("Thinking…", expanded=True)

        def on_event(kind, payload):
            if kind == "tool_call":
                status.write(f"🔧 `{payload['name']}` {payload['arguments']}")
            elif kind == "tool_result" and "error" in payload["output"]:
                status.write(f"⚠️ {payload['output']['error']}")

        try:
            res = run_agent(question, llm, tb, on_event=on_event)
        except LLMError as exc:
            status.update(label="LLM error", state="error")
            st.error(str(exc))
            st.stop()
        status.update(label=f"Done: {len(res.trace)} tool calls, {res.llm_requests} LLM requests",
                      state="complete", expanded=False)
        st.markdown(res.answer)
        if res.cited_pmids:
            bad = res.ungrounded_citations
            if bad:
                st.warning(f"Cited without fetching the abstract: {', '.join(bad)}")
            else:
                st.caption(f"✅ All {len(res.cited_pmids)} citations were fetched and read this turn.")
    st.session_state.history.append((question, res))
