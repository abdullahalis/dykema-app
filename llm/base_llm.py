from abc import ABC, abstractmethod
from typing import List, Dict, Iterator

class BaseLLM(ABC):
    @abstractmethod
    def generate_response(self, messages: List[Dict[str, str]]) -> Iterator[str]:
        pass