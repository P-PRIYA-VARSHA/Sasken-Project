from sentence_transformers import SentenceTransformer
import chromadb

def search_code(query, k=3):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode([query]).tolist()[0]

    client = chromadb.Client(chromadb.config.Settings(
    persist_directory="./chroma_store"
))

    collection = client.get_or_create_collection("code_chunks")

    results = collection.query(query_embeddings=[embedding], n_results=k)

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "code": results["documents"][0][i],
            "file": results["metadatas"][0][i]["file"],
            "start_line": results["metadatas"][0][i]["start_line"],
            "end_line": results["metadatas"][0][i]["end_line"],
        })

    return chunks
