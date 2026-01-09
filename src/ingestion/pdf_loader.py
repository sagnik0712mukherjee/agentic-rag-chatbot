from pathlib import Path
from src.utils.logger import get_logger

logger = get_logger(__name__)

def load_pdf(pdf_path: str) -> Path:
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found at {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Provided file is not a PDF")

    logger.info(f"Loaded PDF: {pdf_path.name}")
    return pdf_path
