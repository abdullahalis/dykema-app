# llm/factory.py
from config.settings import LLM_PROVIDER
from llm.base_llm import BaseLLM
from llm.openai_llm import OpenAILLM
from llm.anthropic_llm import AnthropicLLM

def get_llm() -> BaseLLM:
    if LLM_PROVIDER == "openai":
        return OpenAILLM()
    elif LLM_PROVIDER == "anthropic":
        return AnthropicLLM()
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")
