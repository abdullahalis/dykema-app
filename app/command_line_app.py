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
    """CLI application for interacting with LLM and managing conversations."""

    def __init__(self):
        """Initialize services, storage, LLM, and orchestration manager."""
        setup_logging()
        self.auth_manager = SupabaseAuthManager()
        storage_manager = CombinedStorageManager(SupabaseBackend(), RedisCacheManager())
        llm_manager = LLMManager(llm=get_llm(), retriever=vector_manager)
        self.orchestrator = OrchestrationManager(self.auth_manager, storage_manager, llm_manager)

    def run(self) -> None:
        """Start the application input loop."""
        self._run_loop()

    def _run_loop(self) -> None:
        """Main input loop: reads user input and processes commands or prompts."""
        print("Welcome to the Dykema CLI App!")
        self._ensure_signed_in()
        print("Start a conversation or type /help for more options.")

        while True:
            self._ensure_signed_in()
            user_input = input("> ")
            self._process_input(user_input)

    def _process_input(self, user_input: str) -> None:
        """Route user input to either command handling or LLM processing.

        Args:
            user_input (str): The input entered by the user.
        """
        if user_input.startswith("/"):
            self._process_command(user_input)
        else:
            # Normal user input → LLM
            self.orchestrator.handle_prompt(user_input)

    def _process_command(self, command: str) -> None:
        """Process CLI commands starting with '/'.

        Args:
            command (str): The command input by the user.
        """
        if command == "/help":
            self._print_options()
        elif command == "/logout":
            if self.auth_manager.sign_out():
                print("Signed out.")
            else:
                print("Sign out failed.")
        elif command == "/quit":
            print("Goodbye!")
            exit(0)
        elif command == "/list":
            self.orchestrator.list_conversations()
        elif command == "/select":
            self.orchestrator.list_conversations()
            title = input("Enter conversation title to select (or /cancel to cancel): ")
            if title != "/cancel":
                self.orchestrator.switch_conversation(title)
            else:
                print("Selection cancelled.")
        elif command == "/show":
            self.orchestrator.print_conversation()
        elif command == "/new":
            self.orchestrator.create_new_conversation()
        elif command == "/delete":
            self.orchestrator.list_conversations()
            title = input("Enter conversation title to delete (or /cancel to cancel): ")
            if title != "/cancel":
                self.orchestrator.delete_conversation(title)
            else:
                print("Deletion cancelled.")
        elif command == "/rename":
            new_title = input("Enter new title for the current conversation (or /cancel to cancel): ")
            if new_title != "/cancel":
                self.orchestrator.rename_conversation(new_title)
            else:
                print("Renaming cancelled.")
        else:
            print("Unknown command. Type /help for options.")

    def _ensure_signed_in(self) -> None:
        """Ensure the user is signed in before allowing any operations."""
        # self.auth_manager.sign_in("abdullahalisye@gmail.com", "password")  # TODO: remove
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

    def _print_options(self) -> None:
        """Print all available commands for the user."""
        print(
            """
            Type your message and hit Enter to send it to the LLM or type a command.

            Available commands:
            /logout to sign out
            /quit to quit application
            /new to start a new conversation
            /list to show all conversations
            /select to select a conversation
            /show to show current conversation
            /delete to delete a conversation
            /rename to rename current conversation
            /help to show this help message
            """
        )
