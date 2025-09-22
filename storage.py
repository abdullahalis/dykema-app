from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import config
from supabase import create_client

class StorageManager(ABC):
    """Abstract base class for storage providers"""
    
    @abstractmethod
    def save_conversation(self, user_id: str, conversation_id: str, conversation: List[Dict[str, str]]) -> bool:
        pass
    
    @abstractmethod
    def load_conversation(self, user_id: str, conversation_id: str) -> Optional[Dict[str, Any]]:
        pass
    
    # @abstractmethod
    # def list_conversations(self, user_id: str) -> List[Dict[str, Any]]:
    #     pass
    
    # @abstractmethod
    # def delete_conversation(self, user_id: str, conversation_id: str) -> bool:
    #     pass

class SupabaseStorageManager(StorageManager):
    def __init__(self):
        self.supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
        self.table_name = 'conversations'

    def save_conversation(self, user_id, conversation_id, conversation):
        """Save conversation to Supabase"""
        try:
            # Check if conversation exists
            existing = self.load_conversation(user_id, conversation_id)
            
            if existing:
                # Update existing conversation
                response = (self.supabase
                           .table(self.table_name)
                           .update({"messages": conversation})
                           .eq('id', conversation_id)
                           .eq('user_id', user_id)
                           .execute())
            else:
                # Insert new conversation
                response = (self.supabase
                           .table(self.table_name)
                           .insert(conversation)
                           .execute())
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False
        

    def load_conversation(self, user_id: str, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Load specific conversation from Supabase"""
        try:
            response = (self.supabase
                       .table(self.table_name)
                       .select('messages')
                       .eq('id', conversation_id)
                       .eq('user_id', user_id)
                       .single()
                       .execute())
            return response.data
        except Exception as e:
            return None