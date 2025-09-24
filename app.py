from llm.llm_manager import LLMManager
from llm.factory import get_llm
from config.services import setup_logging
from conversation_manager import ConversationManager
from storage.backend.supabase_backend import SupabaseBackend
from storage.cache.redis_cache import RedisCacheManager
from storage.combined_storage import CombinedStorageManager
from error_types import AuthError
from auth.supabase_auth import SupabaseAuthManager

class App:
    def __init__(self):
        setup_logging()
        self.auth_manager = SupabaseAuthManager()
        self.storage_manager = CombinedStorageManager(SupabaseBackend(), RedisCacheManager())
        self.conversation_manager = ConversationManager(self.auth_manager, self.storage_manager)
        self.llm_manager = LLMManager(get_llm(), self.conversation_manager)

    def run(self):
        self.input_loop()

    def input_loop(self):
        self.check_user()
        print("Start a conversation or /help for more options")

        while True:
            self.check_user()
            user_input = input("> ")
            self.handle_input(user_input)

    def handle_input(self, user_input: str):
        if user_input == "/help":
            self.print_options()
        elif user_input == "/logout":
            if self.auth.sign_out():
                print("Signed out")
            else:
                print("sign out failed")
        elif user_input == "/quit":
            print("Goodbye!")
            exit(0)
        elif user_input == "/list":
            self.conversation_manager.list_conversations()
        elif user_input == "/select": #TODO: allow user to cancel
            self.conversation_manager.list_conversations()
            title = input("Enter conversation title to select: ")
            self.conversation_manager.switch_conversation(title)
        elif user_input == "/show":
            self.conversation_manager.print_conversation()
        elif user_input == "/new":
            self.conversation_manager.create_new_conversation()
        elif user_input == "/delete":
            self.conversation_manager.list_conversations()
            title = input("Enter conversation title to delete: ")
            self.conversation_manager.delete_conversation(title)
        elif user_input == "/rename":
            new_title = input("Enter new title for the current conversation: ")
            self.conversation_manager.rename_conversation(new_title)
        else:  # normal user input → LLM
            self.llm_manager.handle_input(user_input)

    def check_user(self):
        self.auth_manager.sign_in("abdullahalisye@gmail.com", "password")  # TODO: remove
        while self.auth_manager.get_user_id() is None:
            print("Please log in or sign up")
            print("1. Sign In")
            print("2. Sign up")

            choice = input("Enter 1 or 2: ")

            if choice == "1":
                email = input("Email: ")
                password = input("Password: ")

                try:
                    self.auth_manager.sign_in(email, password)
                    print("Successfully signed in as", email)
                except AuthError as e:
                    print(f"Authentication Error: {e}")

            elif choice == "2":
                email = input("Email: ")
                password = input("Password: ")
                confirm_pass = input("Confirm password: ")

                if password == confirm_pass:
                    try:
                        self.auth_manager.sign_up(email, password)
                        print("Successfully created account for", email)
                    except AuthError as e:
                        print(f"Authentication Error: {e}")
                else:
                    print("Passwords do not match. Please try again.")
            else:
                print("Invalid input. Please enter 1 or 2.")

    def print_options(self):
        print(
            """
            /logout to sign out
            /quit to quit application
            /new to start a new conversation
            /list to show all conversations
            /select to select a conversation
            /show to show current conversation
            /delete to delete a conversation
            /rename to rename current conversation
            """
        )
