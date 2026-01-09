from typing import List, Dict

def filter_by_page(
    results: List[Dict],
    min_page: int = None,
    max_page: int = None
) -> List[Dict]:
    filtered = []

    for r in results:
        page = r["metadata"].get("page_number")

        if min_page is not None and page < min_page:
            continue
        if max_page is not None and page > max_page:
            continue

        filtered.append(r)

    return filtered


def filter_empty_text(results: List[Dict]) -> List[Dict]:
    return [r for r in results if r["text"].strip()]
