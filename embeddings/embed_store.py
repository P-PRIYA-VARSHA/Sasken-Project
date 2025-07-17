from sentence_transformers import SentenceTransformer
import chromadb
import os
import pickle
from chromadb.config import Settings


def create_embeddings(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path="./chroma_store")

    collection = client.get_or_create_collection("code_chunks")

    texts = [c["code"] for c in chunks]
    metadatas = [{"file": c["file"], "start_line": c["start_line"], "end_line": c["end_line"]} for c in chunks]
    ids = [f"{c['file']}:{c['start_line']}" for c in chunks]
    embeddings = model.encode(texts).tolist()

    collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)

    with open("embeddings/metadata.pkl", "wb") as f:
        pickle.dump(chunks, f)

    print(f"✅ Indexed {len(texts)} chunks in ChromaDB.")
    def create_embeddings(chunks):
        texts = [chunk['code'] for chunk in chunks]
        metadatas = chunks

        client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="./chroma_store"
    ))      

        collection = client.get_or_create_collection(name="code_chunks")
        for i, text in enumerate(texts):
            collection.add(
                documents=[text],
                metadatas=[metadatas[i]],
                ids=[f"id_{i}"]
            )
    
        client.persist()
        print(f"✅ Indexed {len(texts)} chunks in ChromaDB.")
        print(f"✅ Embeddings created and stored in ./chroma_store")

