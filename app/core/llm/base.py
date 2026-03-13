from abc import ABC, abstractmethod
from typing import List
from app.core.llm.schemas import LLMResponse, EmbeddingResponse

class BaseLLM(ABC):

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> LLMResponse:
        pass

    @abstractmethod
    def embed_text(self, text: str) -> EmbeddingResponse:
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> EmbeddingResponse:
        pass