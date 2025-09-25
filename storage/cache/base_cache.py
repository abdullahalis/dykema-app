from abc import ABC, abstractmethod
from typing import Any, Optional

class CacheManager(ABC):
    """Abstract base class for cache providers."""
    @abstractmethod
    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set a value in the cache with an optional Time To Live in seconds."""
        pass

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache by key. Returns None if not found or expired."""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete a value from the cache by key."""
        pass

