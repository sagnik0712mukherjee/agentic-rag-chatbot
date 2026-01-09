from src.guardrails.pii_guard import contains_pii
from src.utils.logger import get_logger

logger = get_logger(__name__)

def validate_llm_output(answer: str, context_chunks: list) -> str:
    if not answer or len(answer.strip()) < 10:
        raise ValueError("LLM produced empty or weak answer")

    if contains_pii(answer):
        raise ValueError("PII detected in output")

    # Basic hallucination check
    context_text = " ".join([c["text"] for c in context_chunks]).lower()
    answer_lower = answer.lower()

    if not any(phrase in context_text for phrase in answer_lower.split()[:20]):
        logger.warning("Potential hallucination detected")

    return answer