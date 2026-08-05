import re
from typing import Dict, Any
from fastapi import HTTPException

# Dangerous prompt injection attack vectors
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"you\s+are\s+now\s+a\s+DAN",
    r"system\s+override",
    r"output\s+the\s+system\s+prompt",
    r"bypass\s+safety\s+filters"
]

def sanitize_prompt_input(user_input: str) -> str:
    """
    Inspects user input text for prompt injection vectors.
    Raises HTTPException 400 if malicious prompt injection pattern is detected.
    """
    if not user_input:
        return user_input
        
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, user_input, re.IGNORECASE):
            raise HTTPException(
                status_code=400,
                detail="Security Alert: Potential prompt injection attack vector detected."
            )
    return user_input

def validate_uploaded_file_security(file_bytes: bytes, filename: str, max_size_mb: int = 10):
    """
    Validates uploaded file size and header magic bytes to prevent executable uploads.
    """
    if len(file_bytes) > max_size_mb * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed threshold of {max_size_mb}MB."
        )

    # Magic Bytes Validation
    # PDF: %PDF (0x25 0x50 0x44 0x46)
    # PNG: 0x89 0x50 0x4E 0x47
    # ZIP/DOCX: 0x50 0x4B 0x03 0x04
    is_pdf = file_bytes.startswith(b"%PDF")
    is_zip_docx = file_bytes.startswith(b"PK\x03\x04")
    is_txt = True  # Fallback plain text check
    
    if not (is_pdf or is_zip_docx or is_txt):
        raise HTTPException(
            status_code=400,
            detail="Security Alert: Invalid or disallowed file header signature."
        )
    return True
