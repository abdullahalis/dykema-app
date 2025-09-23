# from backend.base_backend import BackendManager
# from typing import Optional, List, Dict, Any
# import config, logging
# from error_types import StorageError




# class SupabaseBackend(BackendManager):
#     def __init__(self):
#         self.supabase = config.supabase
#         self.table_name = 'conversations'

#     def save_conversation(self, user_id, conversation_id, messages):
#         try:
#             if conversation_id:
#                 # Update existing conversation
#                 response = (self.supabase
#                         .table(self.table_name)
#                         .update({"messages": messages})
#                         .eq('id', conversation_id)
#                         .eq('user_id', user_id)
#                         .execute())
#             else:
#                 # Insert new conversation
#                 new_convo = {"user_id": user_id, "messages": messages}
#                 response = (self.supabase
#                         .table(self.table_name)
#                         .insert(new_convo)
#                         .execute())
#             if not response.data:
#                 raise StorageError("No data returned from save operation.")
#             return response.data[0]['id'] # return conversation id
#         except Exception as e:
#             logging.error(f"Supabase storage error: {e}", exc_info=True)
#             raise StorageError(f"Failed to save conversation.") from e

        

#     def get_messages(self, user_id: str, conversation_id: str) -> list:
#         if conversation_id is None:
#             return [] # Return empty list for new conversation
#         try:
#             response = (self.supabase
#                     .table(self.table_name)
#                     .select('messages')
#                     .eq('id', conversation_id)
#                     .eq('user_id', user_id)
#                     .single()
#                     .execute())
#             if not response.data:
#                 raise StorageError("Conversation not found.")
#             return response.data['messages']
#         except Exception as e:
#             logging.error(f"Supabase storage error: {e}", exc_info=True)
#             raise StorageError(f"Failed to get messages.")

    
#     def get_conversations(self, user_id):
#         try:
#             response = (self.supabase
#                        .table(self.table_name)
#                        .select('*')
#                        .eq('user_id', user_id)
#                        .order('created_at', desc=True)
#                        .execute())
#             return response.data
#         except Exception as e:
#             logging.error(f"Supabase storage error: {e}", exc_info=True)
#             raise StorageError(f"Failed to fetch conversations.")
        
#     def get_conversation_id(self, user_id, title):
#         try:
#             response = (self.supabase
#                        .table(self.table_name)
#                        .select('id')
#                        .eq('user_id', user_id)
#                        .eq('title', title)
#                        .single()
#                        .execute())
#             return response.data['id']
#         except Exception as e:
#             logging.error(f"Supabase storage error: {e}", exc_info=True)
#             raise StorageError(f"Failed to fetch conversation with that title.")
    
#     def delete_conversation(self, user_id, conversation_id):
#         try:
#             response = (self.supabase
#                        .table(self.table_name)
#                        .delete()
#                        .eq('id', conversation_id)
#                        .eq('user_id', user_id)
#                        .execute())
#             if not response.data:
#                 raise StorageError("Failed to delete conversation")
#         except Exception as e:
#             logging.error(f"Supabase storage error: {e}", exc_info=True)
#             raise StorageError(f"Failed to delete conversation.")
    
#     def rename_conversation(self, user_id, conversation_id, new_title):
#         try:
#             response = (self.supabase
#                        .table(self.table_name)
#                        .update({"title": new_title})
#                        .eq('id', conversation_id)
#                        .eq('user_id', user_id)
#                        .execute())
#             if not response.data:
#                 raise StorageError("Failed to rename conversation.")
#         except Exception as e:
#             logging.error(f"Supabase storage error: {e}", exc_info=True)
#             raise StorageError(f"Failed to rename conversation.")