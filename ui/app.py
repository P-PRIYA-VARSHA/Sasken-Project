import streamlit as st
import time
import pickle
import os
from generation.rag_pipeline import get_answer_from_llm

# ---------- 1. PAGE CONFIG ----------
st.set_page_config(page_title="Chat with Your Code", layout="wide")
st.title("💬 Chat with Your C/C++ Codebase")

# ---------- 2. SESSION STATE SETUP ----------
if "query_log" not in st.session_state:
    st.session_state.query_log = []

# ---------- 3. MAIN INPUT ----------
query = st.text_input("Ask a question about your code...", autocomplete="on")

# ---------- 4. HANDLE QUERY ----------
if query:
    # Track time
    start = time.time()
    answer, retrieved_chunks = get_answer_from_llm(query)
    end = time.time()
    st.session_state.response_time = end - start

    # Log query
    st.session_state.query_log.append(query)

    # Show Answer
    st.markdown("### 📥 Answer")
    st.markdown(f"{answer}")

    # Show Source Code Chunks
    if retrieved_chunks:
        st.markdown("### 🧩 Code References")
        for chunk in retrieved_chunks:
            st.markdown(f"**📄 {chunk['file']}** (lines {chunk['start_line']}–{chunk['end_line']}):")
            st.code(chunk['code'], language="c")

# ---------- 5. QUERY LOG (Below Chat) ----------
st.markdown("---")
st.markdown("### 🧾 Past Questions:")
for i, q in enumerate(reversed(st.session_state.query_log[-10:]), 1):
    st.markdown(f"**{i}.** {q}")

# ---------- 6. FUNCTION LIST LOADER ----------
def get_function_list():
    try:
        with open("embeddings/metadata.pkl", "rb") as f:
            chunks = pickle.load(f)
        return [
            f"{chunk['file']} ➜ Line {chunk['start_line']} – {chunk['code'].split('(')[0].strip()}"
            for chunk in chunks if '(' in chunk['code']
        ]
    except FileNotFoundError:
        return ["metadata.pkl not found"]

# ---------- 7. SIDEBAR ----------
with st.sidebar:
    st.markdown("### 📌 Function References")
    funcs = get_function_list()
    for func in funcs:
        st.markdown(f"- {func}")

    st.markdown("---")
    st.markdown("### 📊 Metrics")
    st.markdown(f"Total Queries: **{len(st.session_state.query_log)}**")
    if "response_time" in st.session_state:
        st.markdown(f"Avg Response Time: **{st.session_state.response_time:.2f}s**")

    st.markdown("---")
    st.markdown("### 🧾 Query Log")
    for i, q in enumerate(reversed(st.session_state.query_log[-10:]), 1):
        st.markdown(f"**{i}.** {q}")


# ---------- 10. MERMAID DIAGRAM ----------
with st.expander("📈 Show Module Diagram"):
    from diagrams.mermaid_gen import generate_mermaid_diagram
    mermaid_code = generate_mermaid_diagram("lprint")  # change if your folder is different
    st.code(mermaid_code, language="mermaid")
    st.markdown("🧠 Copy & paste the above code into [Mermaid Live Editor](https://mermaid.live) to visualize it.")


