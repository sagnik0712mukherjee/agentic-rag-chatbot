from typing import List, Dict
from src.llm_orchestrator import RAGChatbot
from src.utils.logger import get_logger

logger = get_logger(__name__)


def faithfulness_score(answer: str, context_chunks: List[Dict]) -> float:
    """
    Simple grounding score: how much answer overlaps with context.
    """
    context_text = " ".join(c["text"].lower() for c in context_chunks)
    answer_words = set(answer.lower().split())

    overlap = sum(1 for word in answer_words if word in context_text)
    return overlap / max(len(answer_words), 1)


def relevance_score(answer: str, question: str) -> float:
    """
    Simple relevance heuristic.
    """
    q_words = set(question.lower().split())
    a_words = set(answer.lower().split())
    return len(q_words & a_words) / max(len(q_words), 1)


def evaluate_llm(dataset: List[Dict], index_name: str):
    bot = RAGChatbot(index_name)

    faithfulness_scores = []
    relevance_scores = []

    for item in dataset:
        answer = bot.answer(item["question"])
        context = bot.retriever.retrieve(item["question"])

        faithfulness_scores.append(
            faithfulness_score(answer, context)
        )
        relevance_scores.append(
            relevance_score(answer, item["question"])
        )

    metrics = {
        "Faithfulness": sum(faithfulness_scores) / len(faithfulness_scores),
        "Relevance": sum(relevance_scores) / len(relevance_scores)
    }

    logger.info(f"LLM Evaluation Metrics: {metrics}")
    return metrics
