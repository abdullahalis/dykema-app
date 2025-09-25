from llm.client.base_llm import BaseLLM
from typing import List, Dict, Iterator
from error.error_types import LLMError

class LLMManager:
    """Manages interactions with the LLM, including context building and response generation."""
    def __init__(self, llm: BaseLLM, token_limit: int = 2048, retriever = None):
        self.llm = llm
        self.token_count = 0
        self.token_limit = token_limit
        self.retriever = retriever
    
    def _count_tokens(self, message: str) -> int:
        """Roughly estimate token count in a message."""
        return len(message.split()) * 1.3
    
    def build_context(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Build context for LLM by including as many recent messages as possible within token limit."""
        total_tokens = 0
        context = []
        
        for msg in reversed(messages): # Walk backwards (newest to oldest)
            tokens = self._count_tokens(msg["content"])
            if total_tokens + tokens > self.token_limit:
                break
            total_tokens += tokens
            context.append(msg)

        return list(reversed(context)) # Reverse again to restore chronological order

    def generate_response(self, messages: List[Dict[str, str]]) -> Iterator[str]:
        """Generate a response from the LLM, optionally using RAG if retriever is set."""
        system_prompt = "You are a helpful assistant. Do not use markdown, your responses are displayed in a terminal."

        if self.retriever:
            documents = self.retriever.search(messages[-1]["content"]) # Use latest user message to get context from documents
            context_blocks = []
            for doc in documents:
                context_blocks.append(
                    f"[Source: {doc['filename']}] {doc['content']}"
                )
            system_prompt = (
                "You are a knowledgeable and helpful assistant. Do not use markdown, your responses are displayed in a terminal.\n\n"
                "You have access to reference documents that may or may not be relevant to the user's question. "
                "If the documents are useful, incorporate their information into your answer and cite them clearly "
                "using [Source: filename]. Do not say anything like 'based on the document'. If they are not relevant, ignore them and answer normally using your own knowledge.\n\n"
                "References:\n"
                + "\n\n".join(context_blocks)
            )

        yield from self.llm.generate_response(messages, system_prompt)