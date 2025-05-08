# token_counter.py
import os
import tiktoken
import fitz  # PyMuPDF for PDFs
from docx import Document

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext in {".txt", ".html", ".json", ".csv", ".xml", ".md", ".py"}:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    elif ext == ".pdf":
        try:
            doc = fitz.open(file_path)
            return "\n".join([page.get_text() for page in doc])
        except Exception as e:
            return f"[PDF ERROR] {e}"
    elif ext == ".docx":
        try:
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            return f"[DOCX ERROR] {e}"
    else:
        return None

def count_tokens(text, model="gpt-4-0125-preview"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def main():
    folder_path = "input-files"
    report_lines = []
    total_tokens = 0

    if not os.path.exists(folder_path):
        report_lines.append(f"No folder named '{folder_path}' found.")
    else:
        report_lines.append(f"Scanning files in '{folder_path}':\n")
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if os.path.isfile(filepath):
                text = extract_text(filepath)
                if text:
                    if text.startswith("[PDF ERROR]") or text.startswith("[DOCX ERROR]"):
                        report_lines.append(f"{filename}: {text}")
                    else:
                        tokens = count_tokens(text)
                        total_tokens += tokens
                        report_lines.append(f"{filename}: {tokens} tokens")
                else:
                    report_lines.append(f"{filename}: unsupported or unreadable format.")
        report_lines.append(f"\nTotal tokens: {total_tokens}")

    with open("token_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print("\n".join(report_lines))  # Still show in logs

if __name__ == "__main__":
    main()
