from llm import get_llm

llm = get_llm()

def input_loop():
    while True:
        user_input = input("Enter something (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            print("Exiting the loop.")
            break
        response = stream_collect(user_input)
        # TODO: save to convo history, session data
        
def stream_collect(user_input):
    full_response = []
    for chunk in llm.generate_response(user_input):
        print(chunk, end="", flush=True)
        full_response.append(chunk)
    print()
    return "".join(full_response) 

input_loop()