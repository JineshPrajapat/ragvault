from app.core.llm.registry import LLMRegistry
from app.core.llm.base import BaseLLM
from app.core.llm.provider import *

class LLMManager:

    def __init__(self, default_provider: str = "openai"):
        self._default = default_provider

    def get(self, provider_name: str | None = None) -> BaseLLM:
        name = provider_name or self._default
        return LLMRegistry.get(name)