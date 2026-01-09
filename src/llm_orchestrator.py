from openai import OpenAI
from config.config import OPENAI_API_KEY, LLM_MODEL, LLM_TEMPERATURE
from src.retriever.retriever import Retriever
from src.guardrails.input_guard import validate_user_input
from src.guardrails.output_guard import validate_llm_output
from src.utils.validators import validate_context_strength, compute_confidence
from src.utils.logger import get_logger
from src.memory.conversation_store import ConversationStore

logger = get_logger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)
conversation_store = ConversationStore()

def rewrite_query_with_memory(query: str, memory_text: str) -> str:
    pronouns = ["that", "this", "it", "those", "they"]

    if any(p in query.lower() for p in pronouns) and memory_text:
        return f"""
        Previous context:
        {memory_text}

        Follow-up question:
        {query}

        Rewrite the follow-up as a standalone question.
        """
    return query


class RAGChatbot:
    def __init__(self, index_name: str):
        self.retriever = Retriever(index_name)

    def answer(self, query: str, chat_id: str) -> dict:
        validate_user_input(query)

        memory = conversation_store.get_memory(chat_id)

        # Build memory text for retrieval
        memory_text = " ".join(
            msg["content"]
            for msg in memory.get_short_term()
            if msg["role"] == "assistant"
        )

        rewritten_query = rewrite_query_with_memory(query, memory_text)

        context_chunks = self.retriever.retrieve(rewritten_query)

        
        validate_context_strength(context_chunks)

        memory_block = ""
        if memory.get_summary():
            memory_block += f"Conversation Summary:\n{memory.get_summary()}\n\n"

        for msg in memory.get_short_term():
            memory_block += f"{msg['role'].capitalize()}: {msg['content']}\n"

        context_text = "\n\n".join(
            f"[Page {c['metadata']['page_number']}]\n{c['text']}"
            for c in context_chunks
        )

        system_prompt = (
            "You are a factual assistant.\n"
            "Answer ONLY using the provided context.\n"
            "If the answer is not present, say you do not know.\n"
        )

        user_prompt = f"""
        Conversation Memory:
        {memory_block}

        Context:
        {context_text}

        Question:
        {query}

        Answer:
        """

        response = client.chat.completions.create(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        answer = response.choices[0].message.content.strip()
        answer = validate_llm_output(answer, context_chunks)

        memory.add_message("user", query)
        memory.add_message("assistant", answer)

        citations = []
        seen = set()
        for c in context_chunks:
            key = (c["metadata"]["source"], c["metadata"]["page_number"])
            if key not in seen:
                seen.add(key)
                citations.append({
                    "source": c["metadata"]["source"],
                    "page": c["metadata"]["page_number"]
                })

        confidence = compute_confidence(context_chunks, answer)

        logger.info(f"Answer generated with confidence={confidence['label']}")

        return {
            "answer": answer,
            "citations": citations,
            "confidence": confidence
        }
