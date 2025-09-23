from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

class StorageManager(ABC):
    """Abstract base class for storage providers"""
    @abstractmethod
    def get_messages(self, user_id: str, conversation_id: str) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def get_conversations(self, user_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_conversation_id(self, user_id: str, title: str) -> str:
        pass

    @abstractmethod
    def save_conversation(self, user_id: str, conversation_id: str, messages: List[Dict[str, str]]) -> str:
        pass
    
    @abstractmethod
    def delete_conversation(self, user_id: str, conversation_id: str) -> None:
        pass
    
    @abstractmethod
    def rename_conversation(self, user_id: str, conversation_id: str, new_title: str) -> None:
        pass