from abc import ABC, abstractmethod
from typing import List, Dict, Iterator

class BaseLLM(ABC):
    """Abstract base class for LLM clients."""
    @abstractmethod
    def generate_response(self, messages: List[Dict[str, str]], system_prompt: str) -> Iterator[str]:
        """Generate a response from the LLM given a list of messages."""
        pass