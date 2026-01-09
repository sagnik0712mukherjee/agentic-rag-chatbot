import faiss
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple
from config.config import FAISS_INDEX_DIR, EMBEDDING_DIM
from src.utils.logger import get_logger

logger = get_logger(__name__)


class FaissIndex:
    def __init__(self, index_name: str):
        self.index_name = index_name
        self.index_path = Path(FAISS_INDEX_DIR) / f"{index_name}.index"
        self.index = faiss.IndexFlatIP(EMBEDDING_DIM)  # cosine similarity (normalized)
        self.is_trained = False

    def add_embeddings(self, embeddings: List[List[float]]):
        vectors = np.array(embeddings).astype("float32")

        if not self.is_trained:
            self.is_trained = True

        self.index.add(vectors)
        logger.info(f"Added {len(embeddings)} vectors to FAISS index")

    def save(self):
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))
        logger.info(f"FAISS index saved at {self.index_path}")

    def load(self):
        if not self.index_path.exists():
            raise FileNotFoundError(f"FAISS index not found at {self.index_path}")

        self.index = faiss.read_index(str(self.index_path))
        self.is_trained = True
        logger.info(f"FAISS index loaded from {self.index_path}")

    def search(
        self,
        query_vector: List[float],
        top_k: int = 5
    ) -> Tuple[List[float], List[int]]:
        vector = np.array([query_vector]).astype("float32")
        scores, indices = self.index.search(vector, top_k)

        return scores[0].tolist(), indices[0].tolist()
