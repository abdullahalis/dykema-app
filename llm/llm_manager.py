from llm.base_llm import BaseLLM
from conversation_manager import ConversationManager
from typing import List, Dict
from error_types import LLMError

class LLMManager:
    def __init__(self, llm: BaseLLM, conversation_manager: ConversationManager):
        self.llm = llm
        self.convo_manager = conversation_manager
    
    def handle_input(self, user_input: str) -> None:
        messages = self.convo_manager.get_current_messages()
        messages.append({"role": "user", "content": user_input})
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