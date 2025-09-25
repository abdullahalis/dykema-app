from llm.client.base_llm import BaseLLM
from config.settings import OPENAI_KEY, OPENAI_MODEL
from openai import OpenAI
from typing import List, Dict, Iterator
import logging
from error.error_types import LLMError

class OpenAILLM(BaseLLM):
    """OpenAI LLM client implementation."""
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_KEY)
        
    def generate_response(self, messages: List[Dict[str, str]], system_prompt: str) -> Iterator[str]:
        """Stream response generation from OpenAI LLM."""
        try:    
            stream = self.client.responses.create(
                model=OPENAI_MODEL,
                input=messages,
                instructions=system_prompt,
                stream=True
            )
            for event in stream:
                if event.type == "response.output_text.delta":
                    yield event.delta  # pass text chunks back to caller
                elif event.type == "response.error": # TODO: handle error
                    raise Exception(event.error)
        except Exception as e:
            logging.error(f"LLM error: {e}", exc_info=True)
            raise LLMError("Failed to get response from OpenAI LLM")