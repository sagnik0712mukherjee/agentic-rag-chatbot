import json
from pathlib import Path
from typing import List, Dict
from config.config import FAISS_INDEX_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MetadataStore:
    def __init__(self, index_name: str):
        self.index_name = index_name
        self.metadata_path = Path(FAISS_INDEX_DIR) / f"{index_name}_metadata.json"
        self.metadata: List[Dict] = []

    def add(self, records: List[Dict]):
        """
        Records must be in the same order as embeddings added to FAISS.
        """
        self.metadata.extend(records)
        logger.info(f"Stored metadata for {len(records)} vectors")

    def save(self):
        self.metadata_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2)

        logger.info(f"Metadata saved at {self.metadata_path}")

    def load(self):
        if not self.metadata_path.exists():
            raise FileNotFoundError(f"Metadata file not found at {self.metadata_path}")

        with open(self.metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        logger.info(f"Loaded metadata for {len(self.metadata)} vectors")

    def get(self, index: int) -> Dict:
        return self.metadata[index]
