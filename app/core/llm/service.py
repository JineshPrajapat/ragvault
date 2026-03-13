from app.core.llm.manager import LLMManager
from app.core.llm.base import BaseLLM
from app.core.llm.schemas import LLMResponse, EmbeddingResponse
from typing import List


class LLMService:
    """
    High-level facade for LLM interaction.
    """

    def __init__(self, default_provider: str = "openai"):
        self._manager = LLMManager(default_provider=default_provider)

    def _get_provider(self, provider: str | None = None) -> BaseLLM:
        return self._manager.get(provider)

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        provider: str | None = None,
        temperature: float = 0.2
    ) -> LLMResponse:
        llm = self._get_provider(provider)
        return await llm.generate(system_prompt, user_prompt, temperature)

    async def embed_text(
        self,
        text: str,
        provider: str | None = None
    ) -> EmbeddingResponse:
        llm = self._get_provider(provider)
        return await llm.embed_text(text)

    async def embed_batch(
        self,
        texts: List[str],
        provider: str | None = None
    ) -> EmbeddingResponse:
        llm = self._get_provider(provider)
        return await llm.embed_batch(texts)
