# llm/factory.py
from config.settings import LLM_PROVIDER
from llm.client.base_llm import BaseLLM
from llm.client.openai_llm import OpenAILLM
from llm.client.anthropic_llm import AnthropicLLM

def get_llm() -> BaseLLM:
    """Factory function to get the appropriate LLM client based on configuration."""
    if LLM_PROVIDER == "openai":
        return OpenAILLM()
    elif LLM_PROVIDER == "anthropic":
        return AnthropicLLM()
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")
