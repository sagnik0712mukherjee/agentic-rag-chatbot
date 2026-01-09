import math
from typing import List, Dict
from src.retriever.retriever import Retriever
from src.utils.logger import get_logger

logger = get_logger(__name__)


def recall_at_k(retrieved_pages: List[int], relevant_pages: List[int], k: int) -> float:
    retrieved_k = set(retrieved_pages[:k])
    relevant = set(relevant_pages)
    return len(retrieved_k & relevant) / len(relevant) if relevant else 0.0


def mean_reciprocal_rank(retrieved_pages: List[int], relevant_pages: List[int]) -> float:
    for idx, page in enumerate(retrieved_pages):
        if page in relevant_pages:
            return 1.0 / (idx + 1)
    return 0.0


def ndcg_at_k(retrieved_pages: List[int], relevant_pages: List[int], k: int) -> float:
    dcg = 0.0
    for i, page in enumerate(retrieved_pages[:k]):
        if page in relevant_pages:
            dcg += 1.0 / math.log2(i + 2)

    idcg = sum(
        1.0 / math.log2(i + 2)
        for i in range(min(len(relevant_pages), k))
    )

    return dcg / idcg if idcg > 0 else 0.0


def evaluate_retrieval(dataset: List[Dict], index_name: str, k: int = 5):
    retriever = Retriever(index_name)

    recall_scores = []
    mrr_scores = []
    ndcg_scores = []

    for item in dataset:
        results = retriever.retrieve(item["question"], top_k=k)
        retrieved_pages = [r["metadata"]["page_number"] for r in results]

        recall_scores.append(
            recall_at_k(retrieved_pages, item["relevant_pages"], k)
        )
        mrr_scores.append(
            mean_reciprocal_rank(retrieved_pages, item["relevant_pages"])
        )
        ndcg_scores.append(
            ndcg_at_k(retrieved_pages, item["relevant_pages"], k)
        )

    metrics = {
        "Recall@K": sum(recall_scores) / len(recall_scores),
        "MRR": sum(mrr_scores) / len(mrr_scores),
        "nDCG@K": sum(ndcg_scores) / len(ndcg_scores)
    }

    logger.info(f"Retrieval Evaluation Metrics: {metrics}")
    return metrics
