from typing import List, Dict

class ChatMemory:
    def __init__(self, max_turns: int = 4):
        self.max_turns = max_turns
        self.short_term: List[Dict] = []
        self.summary: str = ""

    def add_message(self, role: str, content: str):
        self.short_term.append({
            "role": role,
            "content": content
        })

        # Keep only last N turns (user + assistant = 2 messages)
        if len(self.short_term) > self.max_turns * 2:
            self.short_term = self.short_term[-self.max_turns * 2:]

    def get_short_term(self) -> List[Dict]:
        return self.short_term

    def update_summary(self, new_summary: str):
        self.summary = new_summary

    def get_summary(self) -> str:
        return self.summary
