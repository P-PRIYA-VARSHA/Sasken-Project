import os
import re

def extract_includes(file_path):
    includes = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                match = re.match(r'#include\s+"(.+\.h)"', line)
                if match:
                    includes.append(match.group(1))
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
    return includes

def generate_mermaid_diagram(folder_path: str) -> str:
    edges = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".c") or file.endswith(".h"):
                file_path = os.path.join(root, file)
                includes = extract_includes(file_path)
                for dep in includes:
                    edges.append((file, dep))

    mermaid = "graph TD;\n"
    for src, dest in edges:
        mermaid += f"    {src} --> {dest};\n"
    return mermaid
