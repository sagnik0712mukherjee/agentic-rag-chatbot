import re
from src.utils.logger import get_logger

logger = get_logger(__name__)

INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"system prompt",
    r"you are chatgpt",
    r"override",
    r"act as"
]

def validate_user_input(query: str) -> None:
    # ✅ Handle None or empty input safely
    if query is None:
        raise ValueError("Empty query received")

    if not isinstance(query, str):
        raise ValueError("Invalid query type")

    query = query.strip()
    if not query:
        raise ValueError("Query cannot be empty")

    query_lower = query.lower()

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, query_lower):
            logger.warning("Prompt injection attempt detected")
            raise ValueError("Unsafe query detected")
