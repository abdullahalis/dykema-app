from llm import get_llm
from conversation_manager import ConversationManager

llm = get_llm()
convo = ConversationManager()

def input_loop():
    while True:
        user_input = input("Enter something (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            print("Exiting the loop.")
            break
        # TODO: handle other inputs
        else:
            convo.addMessage("user", user_input)
            response = stream_collect()
            convo.addMessage("assistant", response)
            
        # TODO: save to convo history, session data
        
def stream_collect():
    full_response = []
    for chunk in llm.generate_response(convo.getHistory()):
        print(chunk, end="", flush=True)
        full_response.append(chunk)
    print()
    return "".join(full_response) 

input_loop()