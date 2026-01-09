from sentence_transformers import SentenceTransformer
from typing import List, Dict
from config.config import EMBEDDING_MODEL
from src.utils.logger import get_logger

logger = get_logger(__name__)

class Embedder:
    """
    Responsible ONLY for generating embeddings.
    No storage, no retrieval, no FAISS logic here.
    """

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def embed_texts(
        self,
        texts: List[str],
        batch_size: int = 32,
        normalize: bool = True
    ) -> List[List[float]]:
        """
        Embed a list of texts in batches.
        """

        logger.info(
            f"Generating embeddings for {len(texts)} texts "
            f"(batch_size={batch_size})"
        )

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            normalize_embeddings=normalize
        )

        return embeddings.tolist()

    def embed_chunks(
        self,
        chunks: List[Dict],
        batch_size: int = 32
    ) -> List[Dict]:
        """
        Takes chunk objects and returns chunk objects
        augmented with embeddings.
        """

        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.embed_texts(
            texts=texts,
            batch_size=batch_size
        )

        embedded_chunks = []

        for chunk, vector in zip(chunks, embeddings):
            embedded_chunks.append({
                "embedding": vector,
                "metadata": chunk["metadata"],
                "text": chunk["text"]
            })

        logger.info("Embedding generation completed")
        return embedded_chunks
