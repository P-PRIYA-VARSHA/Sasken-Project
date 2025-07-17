import os
import re
from typing import List, Dict

def read_c_cpp_files(folder_path: str) -> List[str]:
    code_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.c') or file.endswith('.h'):
                full_path = os.path.join(root, file)
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    code_files.append((file, f.read()))
    return code_files

def extract_code_chunks(file_content: str, filename: str) -> List[Dict]:
    lines = file_content.splitlines()
    chunks = []
    comment = ""
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Capture full comment before function
        if line.startswith("//"):
            comment = line

        # Detect function signature (simple but effective)
        if re.match(r'.*\)\s*{', line):  # Ends with ) {
            func_lines = [line]
            start_line = i + 1
            brace_count = line.count('{') - line.count('}')
            i += 1
            while brace_count > 0 and i < len(lines):
                func_lines.append(lines[i])
                brace_count += lines[i].count('{') - lines[i].count('}')
                i += 1
            code_chunk = "\n".join(func_lines)
            chunks.append({
                "file": filename,
                "comment": comment,
                "code": code_chunk,
                "start_line": start_line,
                "end_line": i
            })
            comment = ""
        else:
            i += 1

    return chunks

def process_code_folder(folder_path: str) -> List[Dict]:
    files = read_c_cpp_files(folder_path)
    all_chunks = []
    for filename, content in files:
        chunks = extract_code_chunks(content, filename)
        all_chunks.extend(chunks)
    return all_chunks
