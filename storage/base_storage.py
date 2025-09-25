from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

class StorageManager(ABC):
    """Abstract base class for storage providers"""
    @abstractmethod
    def get_messages(self, user_id: str, conversation_id: str) -> List[Dict[str, str]]:
        """Retrieve messages for a given user and conversation ID."""
        pass

    @abstractmethod
    def get_conversations(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieve a list of conversations for a given user."""
        pass

    @abstractmethod
    def get_conversation_id(self, user_id: str, title: str) -> str:
        """Retrieve a conversation ID by title for a given user."""
        pass

    @abstractmethod
    def save_conversation(self, user_id: str, conversation_id: str, messages: List[Dict[str, str]]) -> str:
        """Save messages for a given user and conversation ID. Returns the conversation ID."""
        pass
    
    @abstractmethod
    def delete_conversation(self, user_id: str, conversation_id: str) -> None:
        """Delete a conversation for a given user and conversation ID."""
        pass
    
    @abstractmethod
    def rename_conversation(self, user_id: str, conversation_id: str, new_title: str) -> None:
        """Rename a conversation for a given user and conversation ID."""
        pass