"""
Evaluation datasets for RAG system.
These are SMALL, HIGH-QUALITY, MANUALLY VERIFIED.
"""

TESLA_EVAL_DATASET = [
    {
        "question": "What are Tesla's sustainability goals?",
        "relevant_pages": [1, 2, 13, 23]
    },
    {
        "question": "How does Tesla manage climate-related risks?",
        "relevant_pages": [196, 197, 198]
    },
    {
        "question": "What is Tesla’s mission statement?",
        "relevant_pages": [1]
    }
]
