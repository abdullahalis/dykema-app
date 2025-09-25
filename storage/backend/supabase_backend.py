from storage.base_storage import StorageManager
from typing import List, Dict, Any
import logging
from config.services import supabase
from error.error_types import StorageError

class SupabaseBackend(StorageManager):
    """Supabase Postgres database implementation of StorageManager."""
    def __init__(self):
        self.supabase = supabase
        self.table_name = 'conversations'

    def get_messages(self, user_id: str, conversation_id: str) -> List[Dict[str, str]]:
        """Retrieve messages for a given user and conversation ID."""
        if conversation_id is None:
            return [] # Return empty list for new conversation
        try:
            response = (self.supabase
                    .table(self.table_name)
                    .select('messages')
                    .eq('id', conversation_id)
                    .eq('user_id', user_id)
                    .single()
                    .execute())
            if not response.data:
                raise StorageError("Conversation not found.")
            return response.data['messages']
        except Exception as e:
            logging.error(f"Supabase storage error: {e}", exc_info=True)
            raise StorageError(f"Failed to get messages.")

    
    def get_conversations(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieve a list of conversations for a given user."""
        try:
            response = (self.supabase
                       .table(self.table_name)
                       .select('*')
                       .eq('user_id', user_id)
                       .order('created_at', desc=True)
                       .execute())
            return response.data
        except Exception as e:
            logging.error(f"Supabase storage error: {e}", exc_info=True)
            raise StorageError(f"Failed to fetch conversations.")
        

    def get_conversation_id(self, user_id: str, title: str) -> str:
        """Retrieve a conversation ID by title for a given user."""
        try:
            response = (self.supabase
                       .table(self.table_name)
                       .select('id')
                       .eq('user_id', user_id)
                       .eq('title', title)
                       .single()
                       .execute())
            return response.data['id']
        except Exception as e:
            logging.error(f"Supabase storage error: {e}", exc_info=True)
            raise StorageError(f"Failed to fetch conversation with that title.")
        

    def save_conversation(self, user_id: str, conversation_id: str, messages: List[Dict[str, str]]) -> str:
        """Save messages for a given user and conversation ID. Returns the conversation ID."""
        try:
            if conversation_id:
                # Update existing conversation
                response = (self.supabase
                        .table(self.table_name)
                        .update({"messages": messages})
                        .eq('id', conversation_id)
                        .eq('user_id', user_id)
                        .execute())
            else:
                # Insert new conversation
                new_convo = {"user_id": user_id, "messages": messages}
                response = (self.supabase
                        .table(self.table_name)
                        .insert(new_convo)
                        .execute())
            if not response.data:
                raise StorageError("No data returned from save operation.")
            return response.data[0]['id'] # return conversation id
        except Exception as e:
            logging.error(f"Supabase storage error: {e}", exc_info=True)
            raise StorageError(f"Failed to save conversation.") from e
        

    def delete_conversation(self, user_id: str, conversation_id: str) -> None:
        """Delete a conversation for a given user and conversation ID."""
        try:
            response = (self.supabase
                       .table(self.table_name)
                       .delete()
                       .eq('id', conversation_id)
                       .eq('user_id', user_id)
                       .execute())
            if not response.data:
                raise StorageError("Failed to delete conversation")
        except Exception as e:
            logging.error(f"Supabase storage error: {e}", exc_info=True)
            raise StorageError(f"Failed to delete conversation.")
    

    def rename_conversation(self, user_id: str, conversation_id: str, new_title: str) -> None:
        """Rename a conversation for a given user and conversation ID."""
        try:
            response = (self.supabase
                       .table(self.table_name)
                       .update({"title": new_title})
                       .eq('id', conversation_id)
                       .eq('user_id', user_id)
                       .execute())
            if not response.data:
                raise StorageError("Failed to rename conversation.")
        except Exception as e:
            logging.error(f"Supabase storage error: {e}", exc_info=True)
            raise StorageError(f"Failed to rename conversation.")