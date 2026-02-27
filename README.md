# 🚀 RAG Chatbot for Complex PDFs

A **production-style Retrieval-Augmented Generation (RAG) chatbot** that parses complex PDFs containing **text, tables, and images**, converts them into structured knowledge, stores them in a vector database, and enables conversational Q&A with memory, guardrails, and evaluation.

This project intentionally avoids agent overengineering and focuses on **clarity, control, and correctness**.

---

## ✨ Core Features

- 📄 **Advanced PDF Parsing**
  - Mixed content: text, tables, images
  - Layout-aware extraction
  - OCR support for scanned sections
- 🧠 **Semantic Search (RAG)**
  - FAISS vector database
  - Metadata-aware retrieval
- 🤖 **LLM-powered Answers**
  - OpenAI GPT-5.2
  - Strictly grounded in retrieved context
- 💬 **ChatGPT-like UI**
  - Built using Streamlit
  - Multi-chat support
  - Rename chats
  - Persistent chat history
- 🧠 **Conversation Memory**
  - Maintained per chat session
- 🛡️ **Guardrails Beyond Prompts**
  - Input validation
  - Hallucination checks
  - Safety & PII filtering
- 📊 **Evaluation First**
  - Retrieval metrics
  - LLM response quality evaluation

---

## 🏗️ High-Level Architecture

User
↓
Streamlit UI
↓
Input Guardrails
↓
Retriever (FAISS)
↓
Context Validation
↓
LLM (GPT-5.2)
↓
Output Guardrails
↓
Response + Memory Update

---

## 📄 Data Source

This project uses a real-world, highly complex PDF:

**Tesla Impact Report**
- Mixed layouts
- Dense tables
- Charts & images

Source:
https://www.tesla.com/ns_videos/2022-tesla-impact-report.pdf

This document is intentionally chosen to stress-test PDF ingestion pipelines.

---

## 🔄 PDF Ingestion Flow

1. Load PDF
2. Extract:
   - Text blocks
   - Tables (structured)
   - Images (OCR if required)
3. Normalize content into structured JSON
4. Semantic chunking
5. Embedding generation
6. Store vectors + metadata in FAISS

---

## 🔍 Retrieval Strategy

- Vector similarity search using FAISS
- Metadata-based filtering
- Optional reranking
- Top-K context selection

---

## 🛡️ Guardrails (Beyond Prompting)

Guardrails are applied at multiple stages:

### Input Guardrails
- Prompt injection detection
- Unsafe intent filtering

### Retrieval Guardrails
- Context relevance validation
- Empty / weak context detection

### Output Guardrails
- Hallucination checks
- Faithfulness to retrieved context
- PII & sensitive data filtering

---

## 📊 Evaluation Strategy

### Retrieval Evaluation
- Recall@K
- Mean Reciprocal Rank (MRR)
- nDCG

### LLM Evaluation
- Answer relevance
- Faithfulness
- Context utilization
- Safety compliance

Retrieval and generation are evaluated independently.

---

## 🧪 Tech Stack

- **LLM**: OpenAI GPT-5.2
- **Embeddings**: all-MiniLM-L6-v2
- **Vector DB**: FAISS
- **UI**: Streamlit
- **PDF Parsing**: Layout-aware parsing + OCR
- **Evaluation**: RAG & LLM evaluation frameworks
- **Language**: Python

---

## 🚧 Project Status

🟡 Active development

Upcoming milestones:
- Finalize PDF parsing schema
- Add automated evaluation runs
- Improve reranking & chunk compression
- Add caching & observability

---

## 👤 Author

**Sagnik Mukherjee**

🔗 GitHub: https://github.com/sagnikmukherjee
