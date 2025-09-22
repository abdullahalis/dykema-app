from datetime import datetime
from auth import AuthError
import uuid

class ConversationManager():
    def __init__(self, auth, storage):
        self.auth = auth
        self.storage = storage
        self.curr_convo_id = None
    
    def create_new_conversation(self):
        try:
            self.auth.get_user_id()
            self.curr_convo_id = None
            print("Type to start a new conversation")
        except AuthError as e:
            print(f"Authentication Error: {e}")
        

    def add_message(self, role, message):
        try:
            user_id = self.auth.get_user_id()
            new_message = {"role": role, "content": message}

            curr_messages = self.storage.get_messages(user_id, self.curr_convo_id)
            curr_messages.append(new_message)
            response = self.storage.save_conversation(user_id, self.curr_convo_id, curr_messages)
            if response:
                if not self.curr_convo_id:
                    self.curr_convo_id = response.data[0]['id']
            else:
                raise Exception("Couldn't add message")
        except AuthError as e:
            print(f"Authentication Error: {e}")
    
    def get_current_convo(self):
        user_id = self.auth.get_user_id()

        if user_id is not None:
            return self.storage.get_messages(user_id, self.curr_convo_id)
        else:
            raise Exception("couldnt get current user")
    
    def list_conversations(self):
        user_id = self.auth.get_user_id()
        if user_id is not None:
            response = self.storage.list_conversations(user_id)

            if not response:
                print("Problem fetching conversations")
                return 
            conversations = response.data
            if not conversations:
                print("No conversations found.")
                return 
            
            print("Your Conversations:")
            for convo in conversations:
                convo_id = convo['id']
                convo_title = convo.get('title', 'No Title')
                created_at = convo.get('created_at')
                if created_at:
                    created_at = datetime.fromisoformat(created_at).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    created_at = "Unknown"
                prefix = "-> " if convo_id == self.curr_convo_id else "   "
                print(f"{prefix}Title: {convo_title} | Created At: {created_at}")
        else:
            raise Exception("couldnt get user id")

    def switch_conversation(self, title):
        user_id = self.auth.get_user_id()
        if user_id is not None:
            convo_id = self.storage.get_conversation_id(user_id, title)
            if convo_id:
                self.curr_convo_id = convo_id
                print(f"Switched to conversation: {title}")
            else:
                print(f"No conversation found with title: {title}")
        else:
            raise Exception("couldnt get user id")
    
    def print_convo(self):
        user_id = self.auth.get_user_id()
        if user_id is not None:
            messages = self.storage.get_messages(user_id, self.curr_convo_id)
            if not messages:
                print("No messages in this conversation.")
                return
            for msg in messages[-5:]: # print last 5 messages
                role = msg['role']
                content = msg['content']
                print(f"{role.capitalize()}: {content}\n")
    
    def delete_conversation(self, title):
        user_id = self.auth.get_user_id()
        if user_id is not None:
            convo_id = self.storage.get_conversation_id(user_id, title)
            if convo_id:
                success = self.storage.delete_conversation(user_id, convo_id)
                if success:
                    print(f"Deleted conversation: {title}")
                else:
                    print(f"Failed to delete conversation: {title}")
            else:
                print(f"No conversation found with title: {title}")
        else:
            raise Exception("couldnt get user id")

    def rename_conversation(self, new_title):
        if not self.curr_convo_id:
            print("No active conversation to rename.")
            return
        
        user_id = self.auth.get_user_id()
        if user_id is not None:
            success = self.storage.rename_conversation(user_id, self.curr_convo_id, new_title)
            if success:
                print(f"Conversation renamed to: {new_title}")
            else:
                print("Failed to rename conversation.")
        else:
            raise Exception("couldnt get user id")