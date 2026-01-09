import re

PII_PATTERNS = [
    r"\b\d{10}\b",          # phone numbers
    r"\b\d{3}-\d{2}-\d{4}\b",  # SSN-like
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
]

def contains_pii(text: str) -> bool:
    for pattern in PII_PATTERNS:
        if re.search(pattern, text):
            return True
    return False
