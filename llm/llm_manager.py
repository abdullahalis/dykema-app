from llm.client.base_llm import BaseLLM
from typing import List, Dict
from error.error_types import LLMError

class LLMManager:
    def __init__(self, llm: BaseLLM, token_limit: int = 2048, retriever = None):
        self.llm = llm
        self.token_count = 0
        self.token_limit = token_limit
        self.retriever = retriever
    
    def count_tokens(self, message: str) -> int:
        # Simple approximation of token count
        return len(message.split()) * 1.3
    
    def build_context(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        total_tokens = 0
        context = []

        # Walk backwards (newest → oldest)
        for msg in reversed(messages):
            tokens = self.count_tokens(msg["content"])
            if total_tokens + tokens > self.token_limit:
                break
            total_tokens += tokens
            context.append(msg)
        

        # Reverse again to restore chronological order
        return list(reversed(context))

    def generate_response(self, messages: List[Dict[str, str]]):
        # If retriever is enabled, add RAG context
        system_prompt = "You are a helpful assistant. Do not use markdown, your responses are displayed in a terminal."
        if self.retriever:
            docs = self.retriever.search(messages[-1]["content"])
            # Format docs for context
            context_blocks = []
            for d in docs:
                context_blocks.append(
                    f"[Source: {d['filename']}] {d['content']}"
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

    def handle_prompt(self, user_prompt: str) -> None:
        messages = self.build_context(user_prompt)

        response = self.print_stream(messages)
        messages.append({"role": "assistant", "content": response})
        self.convo_manager.update_messages(messages)  

    def print_stream(self, messages: List[Dict[str, str]]) -> None:
        try:
            full_response = []
            for chunk in self.llm.generate_response(messages):
                print(chunk, end="", flush=True)
                full_response.append(chunk)
            print()
            return "".join(full_response) 
        except LLMError as e:
            print(f"LLM Error: {e}")