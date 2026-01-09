from src.utils.logger import get_logger

logger = get_logger(__name__)

def build_document_json(pdf_path, text_pages, tables_by_page):
    document = {
        "document": {
            "source": pdf_path.name,
            "path": str(pdf_path),
            "num_pages": len(text_pages)
        },
        "pages": []
    }

    for page in text_pages:
        page_number = page["page_number"]
        table_info = tables_by_page.get(page_number, {})

        document["pages"].append({
            "page_number": page_number,
            "text": page["text"],
            "tables": table_info.get("tables", []),
            "table_count": table_info.get("table_count", 0),
            "image_count": page.get("image_count", 0),
            "has_images": page.get("has_images", False),
            "images": []  # reserved for selective OCR later
        })

    logger.info(
        f"Built structured JSON with image & table metadata "
        f"for {len(document['pages'])} pages"
    )

    return document
