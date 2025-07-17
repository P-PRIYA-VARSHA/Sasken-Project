from code_parser.chunker import process_code_folder
import os

# Check if folder exists
print("Files in lprint/:", os.listdir("lprint"))

# Parse the code
chunks = process_code_folder("lprint")
print(f"✅ Total chunks extracted: {len(chunks)}")

# Optional: Preview the first chunk
if chunks:
    print("Preview chunk:\n", chunks[0])
