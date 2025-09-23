import config
from openai import OpenAI
import anthropic

class LLMManager:
    def __init__(self, llm, conversation_manager):
        self.llm = llm
        self.convo_manager = conversation_manager

    def handle_input(self, user_input):
        messages = self.convo_manager.get_current_messages()
        messages.append({"role": "user", "content": user_input})
        response = self.print_stream(messages)
        messages.append({"role": "assistant", "content": response})
        self.convo_manager.update_messages(messages)  

    def print_stream(self, messages):
        full_response = []
        for chunk in self.llm.generate_response(messages):
            print(chunk, end="", flush=True)
            full_response.append(chunk)
        print()
        return "".join(full_response) 
    
class BaseLLM:
    def generate_response(self, prompt: str) -> str:
        raise NotImplementedError

class OpenAILLM(BaseLLM):
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_KEY)

    def generate_response(self, prompt: str):
        stream = self.client.responses.create(
            model=config.MODEL,
            input=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            stream=True
        )
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta  # pass text chunks back to caller
            elif event.type == "response.error": # TODO: handle error
                raise Exception(event.error)
        

class AnthropicLLM(BaseLLM):
    def __init__(self):
        self.client = anthropic.Anthropic(
        api_key=config.ANTRHROPIC_KEY,
    )

    def generate_response(self, conversation):
        with self.client.messages.stream(
            max_tokens=1024,
            messages=conversation,
            model=config.ANTHROPIC_MODEL,
        ) as stream:
            for text in stream.text_stream:
                yield text


class MistralLLM(BaseLLM):
    def __init__(self):
        # Would initialize mistral client here
        pass

    def generate_response(self, prompt: str) -> str:
        raise NotImplementedError("Mistral support not implemented yet.")


# Factory method to get appropriate LLM instance
def get_llm() -> BaseLLM:
    if config.LLM_PROVIDER == "openai":
        return OpenAILLM()
    elif config.LLM_PROVIDER == "anthropic":
        return AnthropicLLM()
    elif config.LLM_PROVIDER == "mistral":
        return MistralLLM()
    else:
        raise ValueError(f"Unsupported LLM provider: {config.LLM_PROVIDER}")