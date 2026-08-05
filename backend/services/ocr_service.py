import os
from pypdf import PdfReader

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text content from a PDF file using pypdf.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")
        
    reader = PdfReader(file_path)
    extracted_text = []
    
    for page_idx, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            extracted_text.append(text)
            
    return "\n".join(extracted_text).strip()

def extract_text_from_file(file_path: str) -> str:
    """
    Routes file to appropriate extraction strategy based on file extension.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".txt", ".md"]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()
    else:
        # Fallback basic text read
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()
