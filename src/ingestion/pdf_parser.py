import pdfplumber
import logging
from src.utils.logger import get_logger

# Silence pdfminer noisy graphics warnings
logging.getLogger("pdfminer").setLevel(logging.ERROR)

logger = get_logger(__name__)

def extract_text_blocks(pdf_path):
    pages_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""

            image_count = len(page.images) if page.images else 0

            pages_data.append({
                "page_number": page_num,
                "text": text.strip(),
                "image_count": image_count,
                "has_images": image_count > 0
            })

    logger.info(
        f"Extracted text from {len(pages_data)} pages "
        f"(image-heavy PDF handled safely)"
    )

    return pages_data
