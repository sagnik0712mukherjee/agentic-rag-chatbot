from typing import Dict
from src.memory.chat_memory import ChatMemory

class ConversationStore:
    def __init__(self):
        self.store: Dict[str, ChatMemory] = {}

    def get_memory(self, chat_id: str) -> ChatMemory:
        if chat_id not in self.store:
            self.store[chat_id] = ChatMemory()
        return self.store[chat_id]
