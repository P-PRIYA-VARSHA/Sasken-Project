from code_parser.chunker import process_code_folder
from embeddings.embed_store import create_embeddings

chunks = process_code_folder("lprint")
print(f"✅ Parsed {len(chunks)} chunks")
create_embeddings(chunks)
print("✅ Embeddings created!")
