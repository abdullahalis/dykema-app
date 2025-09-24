from llm.llm_manager import LLMManager

from llm.factory import get_llm
from config.services import setup_logging, vector_manager
from orchestration.orchestration_manager import OrchestrationManager
from storage.backend.supabase_backend import SupabaseBackend
from storage.cache.redis_cache import RedisCacheManager
from storage.combined_storage import CombinedStorageManager
from error.error_types import AuthError
from auth.supabase_auth import SupabaseAuthManager

class CommandLineApp:
    def __init__(self):
        setup_logging()
        self.auth_manager = SupabaseAuthManager()
        storage_manager = CombinedStorageManager(SupabaseBackend(), RedisCacheManager())
        llm_manager = LLMManager(llm=get_llm(), retriever=vector_manager)
        self.orchestration_manager = OrchestrationManager(self.auth_manager, storage_manager, llm_manager)

    def run(self):
        self.input_loop()

    def input_loop(self):
        self.check_user()
        print("Hi! Start a conversation or type /help for more options.")

        while True:
            self.check_user()
            user_input = input("> ")
            self.handle_input(user_input)

    def handle_input(self, user_input: str):
        if user_input.startswith("/"):
                
            if user_input == "/help":
                self.print_options()
            elif user_input == "/logout":
                if self.auth.sign_out():
                    print("Signed out.")
                else:
                    print("Sign out failed.")
            elif user_input == "/quit":
                print("Goodbye!")
                exit(0)
            elif user_input == "/list":
                self.orchestration_manager.list_conversations()
            elif user_input == "/select": #TODO: allow user to cancel
                self.orchestration_manager.list_conversations()
                title = input("Enter conversation title to select (or /cancel to cancel): ")
                if title != "/cancel":
                    self.orchestration_manager.switch_conversation(title)
                else:
                    print("Selection cancelled.")
            elif user_input == "/show":
                self.orchestration_manager.print_conversation()
            elif user_input == "/new":
                self.orchestration_manager.create_new_conversation()
            elif user_input == "/delete":
                self.orchestration_manager.list_conversations()
                title = input("Enter conversation title to delete (or /cancel to cancel): ")
                if title != "/cancel":
                    self.orchestration_manager.delete_conversation(title)
                else:
                    print("Deletion cancelled.")
                self.orchestration_manager.delete_conversation(title)
            elif user_input == "/rename":
                new_title = input("Enter new title for the current conversation (or /cancel to cancel): ")
                self.orchestration_manager.rename_conversation(new_title)
                if new_title != "/cancel":
                    self.orchestration_manager.rename_conversation(new_title)
                else:
                    print("Renaming cancelled.")
            else: # unknown command
                print("Unknown command. Type /help for options.")
        else:  # normal user input → LLM
            self.orchestration_manager.handle_prompt(user_input)

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