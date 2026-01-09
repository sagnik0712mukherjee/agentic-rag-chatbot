import streamlit as st
import uuid

def init_session_state():
    if "chats" not in st.session_state:
        st.session_state.chats = {}

    if "active_chat_id" not in st.session_state:
        chat_id = create_new_chat()
        st.session_state.active_chat_id = chat_id


def create_new_chat():
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {
        "name": "New Chat",
        "messages": []
    }
    return chat_id
