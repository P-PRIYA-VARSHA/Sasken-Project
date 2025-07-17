import ollama
from retrieval.retriever import search_code

def is_general_question(query: str) -> bool:
    general_keywords = ["what is", "define", "explain", "how to", "difference between", "why"]
    return any(k in query.lower() for k in general_keywords)

def get_answer_from_llm(query: str):
    # 1. Handle general questions directly
    if is_general_question(query):
        print("💡 Detected general question – using TinyLlama directly.")
        response = ollama.chat(
            model="tinyllama",
            messages=[{"role": "user", "content": query}]
        )
        return response["message"]["content"], []

    # 2. Retrieve code chunks
    chunks = search_code(query)

    # 3. If nothing found, fall back to general model
    if not chunks:
        print("⚠️ No chunks found – using fallback TinyLlama.")
        response = ollama.chat(
            model="tinyllama",
            messages=[{"role": "user", "content": query}]
        )
        return response["message"]["content"], []

    # 4. Build detailed code context
    print(f"✅ Found {len(chunks)} relevant code chunks.")
    chunk_context = "\n\n".join([
        f"📄 **{c['file']}** (lines {c['start_line']}–{c['end_line']}):\n```c\n{c['code']}\n```"
        for c in chunks
    ])

    # 5. Construct prompt
    prompt = f"""
You are a helpful C/C++ coding assistant.

Context:
{chunk_context}

Question:
{query}

Answer based on the code context above. If the context isn't relevant, answer from your general C/C++ knowledge.
"""

    # 6. Query model (you can use tinyllama or larger if you have RAM)
    response = ollama.chat(
        model="tinyllama",  # Or "mistral", "gemma", etc.
        messages=[{"role": "user", "content": prompt.strip()}]
    )

    return response["message"]["content"].strip(), chunks
