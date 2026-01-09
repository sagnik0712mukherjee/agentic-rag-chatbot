import streamlit as st
from src.app.session_state import init_session_state
from src.app.sidebar import render_sidebar
from src.app.chat_ui import render_chat
from src.llm_orchestrator import RAGChatbot

st.set_page_config(page_title="Tesla RAG Chatbot", layout="wide")

init_session_state()
render_sidebar()

chat_id = st.session_state.active_chat_id
chat = st.session_state.chats[chat_id]

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

st.title(chat["name"])

# 🔑 Always render ONLY from state
render_chat(chat["messages"])

query = st.chat_input("Ask about Tesla Impact Report...")

if query:
    # Save query in session state (CRITICAL)
    st.session_state.pending_query = query

    # Append user message
    chat["messages"].append({
        "role": "user",
        "content": query
    })

    # Append thinking placeholder
    chat["messages"].append({
        "role": "assistant",
        "content": "🤔 Thinking..."
    })

    st.rerun()

# Handle thinking state safely
if (
    chat["messages"]
    and chat["messages"][-1]["content"] == "🤔 Thinking..."
    and st.session_state.pending_query is not None
):
    bot = RAGChatbot(index_name="tesla_impact_report")

    result = bot.answer(
        st.session_state.pending_query,
        chat_id
    )

    # Replace thinking message with final answer
    chat["messages"][-1] = {
        "role": "assistant",
        "content": result["answer"],
        "confidence": result["confidence"],
        "citations": result["citations"]
    }

    # Clear pending query (CRITICAL)
    st.session_state.pending_query = None

    st.rerun()
