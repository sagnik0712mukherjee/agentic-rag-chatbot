from config.config import CHUNK_SIZE, CHUNK_OVERLAP
from src.utils.logger import get_logger

logger = get_logger(__name__)

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks

def chunk_document(document_json):
    chunks = []

    for page in document_json["pages"]:
        page_text = page["text"]
        if not page_text:
            continue

        page_chunks = chunk_text(page_text)

        for idx, chunk in enumerate(page_chunks):
            chunks.append({
                "text": chunk,
                "metadata": {
                    "page_number": page["page_number"],
                    "chunk_index": idx,
                    "source": document_json["document"]["source"]
                }
            })

    logger.info(f"Generated {len(chunks)} chunks")
    return chunks
