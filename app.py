from llm import get_llm, LLMManager
from conversation_manager import ConversationManager
from auth import SupabaseAuthManager
from storage.backend.supabase_backend import SupabaseBackend
from storage.cache.redis_cache import RedisCacheManager
from storage.combined_storage import CombinedStorageManager
from error_types import AuthError

auth = SupabaseAuthManager()
storage_manager = CombinedStorageManager(SupabaseBackend(), RedisCacheManager())
convo = ConversationManager(auth, storage_manager)
llm = get_llm()
llm_manager = LLMManager(llm, convo)

def input_loop():
    check_user()
    print("Start a conversation or /help for more options")
    while True:
        check_user()
        user_input = input("> ")
        handle_input(user_input)
        # TODO: save to convo history, session data

def handle_input(user_input):
    if user_input == "/help":
        print_options()
    elif user_input == "/logout":
        if auth.sign_out():
            print("Signed out")
        else:
            print("sign out failed")
    elif user_input == "/quit":
        print("Goodbye!")
        exit(0)
    elif user_input == "/list":
        convo.list_conversations()
    elif user_input == "/select":
        convo.list_conversations()
        title = input("Enter conversation title to select: ")
        convo.switch_conversation(title)
    elif user_input == "/show":
        convo.print_convo()
    elif user_input == "/new":
        convo.create_new_conversation()
    elif user_input == "/delete":
        convo.list_conversations()
        title = input("Enter conversation title to delete: ")
        convo.delete_conversation(title)
    elif user_input == "/rename":
        new_title = input("Enter new title for the current conversation: ")
        convo.rename_conversation(new_title)
    else: # if not a command, send to llm
        llm_manager.handle_input(user_input)

def print_options():
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
        """)

# def get_llm_response(user_input):
#     messages = convo.get_current_messages()
#     messages.append({"role": "user", "content": user_input})
#     response = stream_collect(messages)
#     messages.append({"role": "assistant", "content": response})
#     convo.update_messages(messages)  

# def stream_collect(messages):
#     full_response = []
#     for chunk in llm.generate_response(messages):
#         print(chunk, end="", flush=True)
#         full_response.append(chunk)
#     print()
#     return "".join(full_response) 

def check_user():
    
    auth.sign_in("abdullahalisye@gmail.com", "password") # TODO: remove 
    while auth.get_user_id() is None:

        print("Please log in or sign up")
        print("1. Sign In")
        print("2. Sign up")

        choice = input("Enter 1 or 2: ")

        if choice == "1":
            email = input("Email: ")
            password = input("Password: ")

            try:
                auth.sign_in(email, password)
                print("Succesfuly signed in as", email)
            except AuthError as e:
                print(f"Authentication Error: {e}")
        
        elif choice == "2":
            email = input("Email: ")
            password = input("Password: ")
            confirm_pass = input("Confirm password: ")

            if password == confirm_pass:
                try:
                    auth.sign_up(email, password)
                    print("Successfully created account for", email)
                except AuthError as e:
                    print(f"Authentication Error: {e}")
            else:
                print("Passwords do not match. Please try again.")
        
        else:
            print("Invalid input. Please enter 1 or 2.")

input_loop()