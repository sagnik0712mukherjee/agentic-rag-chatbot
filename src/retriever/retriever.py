from typing import List, Dict
from src.embeddings.embedder import Embedder
from src.vectordb.faiss_index import FaissIndex
from src.vectordb.metadata_store import MetadataStore
from src.retriever.filters import filter_empty_text
from src.retriever.reranker import simple_score_rerank
from config.config import TOP_K
from src.utils.logger import get_logger

logger = get_logger(__name__)


class Retriever:
    def __init__(self, index_name: str):
        self.embedder = Embedder()
        self.index = FaissIndex(index_name)
        self.metadata_store = MetadataStore(index_name)

        # Load persisted index & metadata
        self.index.load()
        self.metadata_store.load()

        logger.info("Retriever initialized successfully")

    def retrieve(
        self,
        query: str,
        top_k: int = TOP_K
    ) -> List[Dict]:
        """
        Returns retrieved context blocks with text + metadata + score.
        """

        logger.info(f"Retrieving context for query: {query}")

        # Embed query
        query_vector = self.embedder.embed_texts([query])[0]

        # Search FAISS
        scores, indices = self.index.search(query_vector, top_k)

        results = []

        for score, idx in zip(scores, indices):
            if idx == -1:
                continue

            metadata = self.metadata_store.get(idx)

            results.append({
                "text": metadata.get("text", ""),
                "metadata": metadata,
                "score": float(score)
            })

        # Filters
        results = filter_empty_text(results)

        # Rerank
        results = simple_score_rerank(results)

        logger.info(f"Retrieved {len(results)} context chunks")

        return results
