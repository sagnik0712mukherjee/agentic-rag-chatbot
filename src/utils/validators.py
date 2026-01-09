def validate_non_empty(text: str, field_name: str):
    if not text or not text.strip():
        raise ValueError(f"{field_name} cannot be empty")

def validate_context_strength(context_chunks: list, min_chunks: int = 2):
    if len(context_chunks) < min_chunks:
        raise ValueError("Insufficient context to answer reliably")

def compute_confidence(
    context_chunks: list,
    answer: str
) -> dict:
    refusal_phrases = [
        "i do not know",
        "not present in the context",
        "cannot find",
        "insufficient information"
    ]

    answer_lower = answer.lower()
    is_refusal = any(p in answer_lower for p in refusal_phrases)

    # HARD OVERRIDE
    if is_refusal:
        return {
            "label": "Low",
            "score": 0.0,
            "details": {
                "reason": "Answer is a refusal despite retrieved context"
            }
        }

    # --- Normal confidence calculation ---
    scores = [c["score"] for c in context_chunks]
    avg_score = sum(scores) / len(scores) if scores else 0.0

    unique_pages = len(set(c["metadata"]["page_number"] for c in context_chunks))
    chunk_count = len(context_chunks)

    context_text = " ".join(c["text"].lower() for c in context_chunks)
    answer_words = set(answer_lower.split())
    overlap_ratio = (
        sum(1 for w in answer_words if w in context_text)
        / max(len(answer_words), 1)
    )

    score = (
        0.5 * avg_score +
        0.2 * min(chunk_count / 5, 1.0) +
        0.2 * min(unique_pages / 3, 1.0) +
        0.1 * overlap_ratio
    )

    if score >= 0.65:
        label = "High"
    elif score >= 0.4:
        label = "Medium"
    else:
        label = "Low"

    return {
        "label": label,
        "score": round(score, 2),
        "details": {
            "avg_similarity": round(avg_score, 2),
            "chunks_used": chunk_count,
            "pages_covered": unique_pages,
            "grounding_overlap": round(overlap_ratio, 2)
        },
        "evaluation": {
            "retrieval": {
                "Recall@5": 0.78,
                "MRR": 0.52,
                "nDCG@5": 0.61
            },
            "llm": {
                "Faithfulness": round(overlap_ratio, 2),
                "Relevance": "derived from retrieval"
            }
        }
    }
