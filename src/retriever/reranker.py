from typing import List, Dict

def simple_score_rerank(results: List[Dict]) -> List[Dict]:
    """
    Placeholder reranker.
    Currently sorts by FAISS similarity score (descending).
    """

    return sorted(results, key=lambda x: x["score"], reverse=True)
