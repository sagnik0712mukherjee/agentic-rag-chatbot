import streamlit as st
from src.app.session_state import create_new_chat

def render_sidebar():
    st.sidebar.title("💬 Chats")

    if "renaming_chat_id" not in st.session_state:
        st.session_state.renaming_chat_id = None

    if st.sidebar.button("➕ Start a New Chat"):
        chat_id = create_new_chat()
        st.session_state.active_chat_id = chat_id
        st.session_state.renaming_chat_id = None
        st.rerun()

    for chat_id, chat in st.session_state.chats.items():
        is_active = chat_id == st.session_state.active_chat_id

        label = f"👉 {chat['name']}" if is_active else chat["name"]

        col1, col2 = st.sidebar.columns([4, 1])

        if col1.button(label, key=f"select_{chat_id}"):
            st.session_state.active_chat_id = chat_id
            st.session_state.renaming_chat_id = None
            st.rerun()

        if col2.button("✏️", key=f"edit_{chat_id}"):
            st.session_state.renaming_chat_id = chat_id

        if st.session_state.renaming_chat_id == chat_id:
            new_name = st.sidebar.text_input(
                "Rename chat",
                value=chat["name"],
                key=f"rename_input_{chat_id}"
            )

            if st.sidebar.button("✅ Save", key=f"save_{chat_id}"):
                if new_name.strip():
                    chat["name"] = new_name.strip()
                st.session_state.renaming_chat_id = None
                st.rerun()
