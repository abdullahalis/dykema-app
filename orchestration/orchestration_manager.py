from datetime import datetime
from error.error_types import AuthError, StorageError, LLMError
from typing import List, Dict
from storage.base_storage import StorageManager
from auth.base_auth import AuthManager
from llm.llm_manager import LLMManager

class OrchestrationManager:
    """Manages orchestration between Auth, Storage, and LLM components."""
    def __init__(self, auth_manager: AuthManager, storage_manager: StorageManager, llm_manager: LLMManager):
        self.auth_manager = auth_manager
        self.storage_manager = storage_manager
        self.llm_manager = llm_manager
        self.curr_convo_id = None
    
    def handle_prompt(self, prompt: str) -> None:
        """
        Process a user prompt: build context, generate response, and update conversation.
        """
        try:
            all_messages = self._get_current_messages() or []
            all_messages.append({"role": "user", "content": prompt})

            context = self.llm_manager.build_context(all_messages)
            response = self._print_stream(context)
            if not response:
                response = "Error: no response generated from LLM."

            all_messages.append({"role": "assistant", "content": response})
            self._update_messages(all_messages)

        except LLMError as e:
            print(f"LLM Error: {e}")
        except AuthError as e:
            print(f"Authentication Error: {e}")
        except StorageError as e:
            print(f"Storage Error: {e}")
        except Exception as e:
            print(f"Unexpected error processing prompt: {e}")

    def create_new_conversation(self) -> None:
        try:
            self.auth_manager.get_user_id()
            self.curr_convo_id = None
            print("Type to start a new conversation")
        except AuthError as e:
            print(f"Authentication Error: {e}")
    
    def list_conversations(self) -> None:
        """Print a list of the user's conversations."""
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

    def switch_conversation(self, title: str) -> None:
        try:
            user_id = self.auth_manager.get_user_id()
            convo_id = self.storage_manager.get_conversation_id(user_id, title)
            self.curr_convo_id = convo_id
            print(f"Switched to conversation: {title}")
        except AuthError as e:
            print(f"Authentication Error: {e}")
        except StorageError as e:
            print(f"Storage Error: {e}")
    
    def print_conversation(self) -> None:
        """Print the last few messages of the current conversation, handling errors and overly long histories."""
        try:
            messages = self._get_current_messages()
            if not messages:
                print("No messages in this conversation. Select a conversation (/select) or start a new one (/new).")
                return

            max_display = 10
            if len(messages) > max_display:
                print(f"Showing the last {max_display} messages (conversation is too long to display entirely):\n")
            else:
                print("Conversation:\n")

            for msg in messages[-max_display:]:
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                print(f"{role.capitalize()}: {content}\n")

        except Exception as e:
            print(f"Error displaying conversation: {e}")
    
    def delete_conversation(self, title: str) -> None:
        try:
            user_id = self.auth_manager.get_user_id()
            convo_id = self.storage_manager.get_conversation_id(user_id, title)
            self.storage_manager.delete_conversation(user_id, convo_id)
            print(f"Deleted conversation: {title}")
        except AuthError as e:
            print(f"Authentication Error: {e}")
        except StorageError as e:
            print(f"Storage Error: {e}")

    def rename_conversation(self, new_title: str) -> None:
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
    
    def _print_stream(self, messages: List[Dict[str, str]]) -> str:
        """Print the LLM response as it streams in and return the full response."""
        try:
            full_response = []
            for chunk in self.llm_manager.generate_response(messages):
                print(chunk, end="", flush=True)
                full_response.append(chunk)
            print()
            return "".join(full_response) 
        except LLMError as e:
            print(f"LLM Error: {e}")
    
    def _update_messages(self, messages: List[Dict[str, str]]) -> None:
        """Save updated messages to storage."""
        try:
            user_id = self.auth_manager.get_user_id()
            convo_id = self.storage_manager.save_conversation(user_id, self.curr_convo_id, messages)
            
            if not self.curr_convo_id:
                self.curr_convo_id = convo_id
        except AuthError as e:
            print(f"Authentication Error: {e}")
        except StorageError as e:
            print(f"Storage Error: {e}")
    
    def _get_current_messages(self) -> List[Dict[str, str]]:
        try:
            user_id = self.auth_manager.get_user_id()
            return self.storage_manager.get_messages(user_id, self.curr_convo_id)
        except AuthError as e:
            print(f"Authentication Error: {e}")
        except StorageError as e:
            print(f"Storage Error: {e}")