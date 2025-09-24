from datetime import datetime
from error_types import AuthError, StorageError

class ConversationManager():
    def __init__(self, auth_manager, storage_manager):
        self.auth_manager = auth_manager
        self.storage_manager = storage_manager
        self.curr_convo_id = None
    
    def create_new_conversation(self):
        try:
            self.auth_manager.get_user_id()
            self.curr_convo_id = None
            print("Type to start a new conversation")
        except AuthError as e:
            print(f"Authentication Error: {e}")
        

    def update_messages(self, messages):
        try:
            user_id = self.auth_manager.get_user_id()
            convo_id = self.storage_manager.save_conversation(user_id, self.curr_convo_id, messages)
            
            if not self.curr_convo_id:
                self.curr_convo_id = convo_id
        except AuthError as e:
            print(f"Authentication Error: {e}")
        except StorageError as e:
            print(f"Storage Error: {e}")
    
    def get_current_messages(self):
        try:
            user_id = self.auth_manager.get_user_id()
            return self.storage_manager.get_messages(user_id, self.curr_convo_id)
        except AuthError as e:
            print(f"Authentication Error: {e}")
        except StorageError as e:
            print(f"Storage Error: {e}")
    
    def list_conversations(self):
        try:
            user_id = self.auth_manager.get_user_id()
            conversations = self.storage_manager.get_conversations(user_id)
            
            print("Your Conversations:")
            for convo in conversations:
                convo_id = convo['id']
                convo_title = convo.get('title', 'No Title')
                updated_at = convo['updated_at']
                updated_at = datetime.fromisoformat(updated_at).strftime('%Y-%m-%d %H:%M:%S')

                prefix = "-> " if convo_id == self.curr_convo_id else "   "
                print(f"{prefix}Title: {convo_title} | Last Updated: {updated_at}")
        except AuthError as e:
            print(f"Authentication Error: {e}")
        except StorageError as e:
            print(f"Storage Error: {e}")

    def switch_conversation(self, title):
        try:
            user_id = self.auth_manager.get_user_id()
            convo_id = self.storage_manager.get_conversation_id(user_id, title)
            self.curr_convo_id = convo_id
            print(f"Switched to conversation: {title}")
        except AuthError as e:
            print(f"Authentication Error: {e}")
        except StorageError as e:
            print(f"Storage Error: {e}")
    
    def print_conversation(self):
        messages = self.get_current_messages()
        if not messages:
            print("No messages in this conversation. Select a conversation (/select) or start a new one (/new).")
            return
        for msg in messages[-5:]: # print last 5 messages
            role = msg['role']
            content = msg['content']
            print(f"{role.capitalize()}: {content}\n")

    
    def delete_conversation(self, title):
        try:
            user_id = self.auth_manager.get_user_id()
            convo_id = self.storage_manager.get_conversation_id(user_id, title)
            self.storage_manager.delete_conversation(user_id, convo_id)
            print(f"Deleted conversation: {title}")
        except AuthError as e:
            print(f"Authentication Error: {e}")
        except StorageError as e:
            print(f"Storage Error: {e}")

    def rename_conversation(self, new_title):
        if not self.curr_convo_id:
            print("No active conversation to rename.")
            return
        
        try:
            user_id = self.auth_manager.get_user_id()
            self.storage_manager.rename_conversation(user_id, self.curr_convo_id, new_title)
            print(f"Conversation renamed to: {new_title}")
        except AuthError as e:
            print(f"Authentication Error: {e}")
        except StorageError as e:
            print(f"Storage Error: {e}")