from abc import ABC, abstractmethod
from typing import Any, Optional

class CacheManager(ABC):
    @abstractmethod
    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass

