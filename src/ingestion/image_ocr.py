import pytesseract
from PIL import Image
from src.src.utils.logger import get_logger

logger = get_logger(__name__)

def ocr_image(image: Image.Image, lang: str = "eng") -> str:
    try:
        text = pytesseract.image_to_string(image, lang=lang)
        return text.strip()
    except Exception as e:
        logger.error(f"OCR failed: {e}")
        return ""
