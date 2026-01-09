import pdfplumber
from src.utils.logger import get_logger

logger = get_logger(__name__)

def extract_tables(pdf_path):
    tables_by_page = {}

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            raw_tables = page.extract_tables() or []
            structured_tables = []

            for table in raw_tables:
                if not table:
                    continue

                structured_tables.append({
                    "rows": table,
                    "num_rows": len(table),
                    "num_columns": len(table[0]) if table and table[0] else 0
                })

            tables_by_page[page_num] = {
                "tables": structured_tables,
                "table_count": len(structured_tables)
            }

    logger.info("Extracted tables with page-level metadata")
    return tables_by_page
