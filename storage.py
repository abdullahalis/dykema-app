from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import config


class StorageManager(ABC):
    """Abstract base class for storage providers"""
    
    @abstractmethod
    def save_conversation(self, user_id: str, conversation_id: str, conversation: List[Dict[str, str]]) -> bool:
        pass
    
    # @abstractmethod
    # def load_conversation(self, user_id: str, conversation_id: str) -> Optional[Dict[str, Any]]:
    #     pass
    
    # @abstractmethod
    # def list_conversations(self, user_id: str) -> List[Dict[str, Any]]:
    #     pass
    
    # @abstractmethod
    # def delete_conversation(self, user_id: str, conversation_id: str) -> bool:
    #     pass

class SupabaseStorageManager(StorageManager):
    def __init__(self):
        self.supabase = config.supabase
        self.table_name = 'conversations'

    def save_conversation(self, user_id, conversation_id, messages):
        """Save conversation to Supabase"""
        try:
            if conversation_id is not None:
                # Update existing conversation
                print("updating convo")
                response = (self.supabase
                           .table(self.table_name)
                           .update({"messages": messages})
                           .eq('id', conversation_id)
                           .eq('user_id', user_id)
                           .execute())
                return response
            else:
                print("inserting new convo")
                print("user from convo manager", user_id)
                print("user from supabase", self.supabase.auth.get_user().user.id)
                # Insert new conversation
                new_convo = {"user_id": user_id, "messages": messages}
                response = (self.supabase
                           .table(self.table_name)
                           .insert(new_convo)
                           .execute())
                return response
        except Exception as e:
            print(f"Save error: {e}")
            return None
        

    def get_messages(self, user_id: str, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Load specific conversation from Supabase"""
        if conversation_id is None:
            return []  # Return empty messages if no conversation selected
        try:
            response = (self.supabase
                       .table(self.table_name)
                       .select('messages')
                       .eq('id', conversation_id)
                       .eq('user_id', user_id)
                       .single()
                       .execute())
            return response.data['messages']
        except Exception as e:
            print(f"Error getting messages: {e}")
            return None
    
    def list_conversations(self, user_id):
        try:
            response = (self.supabase
                       .table(self.table_name)
                       .select('*')
                       .eq('user_id', user_id)
                       .order('created_at', desc=True)
                       .execute())
            return response
        except Exception as e:
            print(f"List error: {e}")
            return None
        
    def get_conversation_id(self, user_id, title):
        try:
            response = (self.supabase
                       .table(self.table_name)
                       .select('id')
                       .eq('user_id', user_id)
                       .eq('title', title)
                       .single()
                       .execute())
            if response.data:
                return response.data['id']
            return None
        except Exception as e:
            print(f"Get ID error: {e}")
            return None
    
    def delete_conversation(self, user_id, conversation_id):
        try:
            response = (self.supabase
                       .table(self.table_name)
                       .delete()
                       .eq('id', conversation_id)
                       .eq('user_id', user_id)
                       .execute())
            return True if response.data else False
        except Exception as e:
            print(f"Delete error: {e}")
            return False
    
    def rename_conversation(self, user_id, conversation_id, new_title):
        try:
            response = (self.supabase
                       .table(self.table_name)
                       .update({"title": new_title})
                       .eq('id', conversation_id)
                       .eq('user_id', user_id)
                       .execute())
            return True if response.data else False
        except Exception as e:
            print(f"Rename error: {e}")
            return False