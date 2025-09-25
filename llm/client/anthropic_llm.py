from llm.client.base_llm import BaseLLM
from config.settings import ANTHROPIC_KEY, ANTHROPIC_MODEL
import anthropic
from typing import List, Dict, Iterator
import logging
from error.error_types import LLMError

class AnthropicLLM(BaseLLM):
    """Anthropic LLM client implementation."""
    def __init__(self):
        self.client =  anthropic.Anthropic(
                        api_key=ANTHROPIC_KEY,
                    )

    def generate_response(self, messages: List[Dict[str, str]], system_prompt: str) -> Iterator[str]:
        """Stream response generation from Anthropic LLM."""
        try:
            with self.client.messages.stream(
                max_tokens=1024,
                system=system_prompt,
                messages=messages,
                model=ANTHROPIC_MODEL,
            ) as stream:
                for text in stream.text_stream:
                    yield text
        except Exception as e:
            logging.error(f"LLM error: {e}", exc_info=True)
            raise LLMError("Failed to get response from Anthropic LLM")