from generation.rag_pipeline import get_answer_from_llm

question = "What is a pointer in C?"
answer = get_answer_from_llm(question)

print("Question:", question)
print("Answer:\n", answer)
