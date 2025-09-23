from storage.base_storage import StorageManager
from typing import List, Dict, Any

class CombinedStorageManager(StorageManager):
    def __init__(self, backend, cache):
        self.backend = backend
        self.cache = cache
    
    def get_messages(self, user_id: str, conversation_id: str) -> List[Dict[str, str]]:
        if not conversation_id:
            return [] # Return empty list for new conversation
        
        cache_key = f"{user_id}:{conversation_id}:messages"
        cached = self.cache.get(cache_key)
        if cached:
            print("Cache hit for messages")
            return cached
        messages = self.backend.get_messages(user_id, conversation_id)
        self.cache.set(cache_key, messages)
        return messages

    def get_conversations(self, user_id: str) -> List[Dict[str, Any]]:
        cache_key = f"{user_id}:conversations"
        cached = self.cache.get(cache_key)
        if cached:
            print("Cache hit for conversations")
            return cached

        conversations = self.backend.get_conversations(user_id)
        self.cache.set(cache_key, conversations)
        return conversations

    def get_conversation_id(self, user_id: str, title: str) -> str:
        # Unnecessary to cache this
        return self.backend.get_conversation_id(user_id, title)

    def save_conversation(self, user_id: str, conversation_id: str, messages: List[Dict[str, str]]) -> None:
        convo_id = self.backend.save_conversation(user_id, conversation_id, messages)

        # Invalidate cache for messages
        cache_key = f"{user_id}:{convo_id}:messages"
        self.cache.set(cache_key, messages)

        # Invalidate full conversation list cache
        list_key = f"{user_id}:conversations"
        self.cache.delete(list_key)

        return convo_id
    
    def delete_conversation(self, user_id: str, conversation_id: str) -> None:
        self.backend.delete_conversation(user_id, conversation_id)

        # Invalidate caches
        self.cache.delete(f"{user_id}:{conversation_id}:messages")
        self.cache.delete(f"{user_id}:conversations")
    
    def rename_conversation(self, user_id: str, conversation_id: str, new_title: str) -> None:
        self.backend.rename_conversation(user_id, conversation_id, new_title)

        # Invalidate caches
        self.cache.delete(f"{user_id}:conversations")
    
