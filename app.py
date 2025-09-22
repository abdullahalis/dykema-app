from llm import get_llm
from conversation_manager import ConversationManager
from auth import SupabaseAuthManager
from storage import SupabaseStorageManager

llm = get_llm()

auth = SupabaseAuthManager()
storage = SupabaseStorageManager()
convo = ConversationManager(auth, storage)

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
    else:
        get_llm_response(user_input)

def print_options():
    print(
        """
        /logout to sign out
        /new to start a new conversation
        /list to show all conversations
        /switch to switch conversation
        /quit to quit application
        """)

def get_llm_response(user_input):
    convo.add_message("user", user_input)
    response = stream_collect()
    convo.add_message("assistant", response)  

def stream_collect():
    full_response = []
    messages = convo.get_current_convo()
    for chunk in llm.generate_response(messages):
        print(chunk, end="", flush=True)
        full_response.append(chunk)
    print()
    return "".join(full_response) 

def check_user():
    while auth.get_user_id() is None:

        print("Please log in or sign up")
        print("1. Sign In")
        print("2. Sign up")

        choice = input("Enter 1 or 2: ")

        if choice == "1":
            email = input("Email: ")
            password = input("Password: ")

            if auth.sign_in(email, password):
                print("Succesfuly signed in as", email)
            else:
                print("Sign in failed")
        
        elif choice == "2":
            email = input("Email: ")
            password = input("Password: ")
            confirm_pass = input("Confirm password: ")

            if password == confirm_pass:
                if auth.sign_up(email, password):
                    print("Successfully created account for", email)
                else:
                    print("Sign up failed")
            else:
                print("Passwords do not match")
        
        else:
            print("invalid input")

input_loop()