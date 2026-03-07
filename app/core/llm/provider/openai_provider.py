# llm/providers/openai_provider.py
from openai import OpenAI
from config import settings
from app.core.llm.base import BaseLLM
from app.core.llm.schemas import LLMResponse, EmbeddingResponse
from app.core.llm.registry import LLMRegistry


class OpenAIProvider(BaseLLM):

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate(self, system_prompt, user_prompt, temperature=0.2):
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )

            return LLMResponse(
                success=True,
                content=response.choices[0].message.content,
                tokens_used=response.usage.total_tokens if response.usage else None
            )

        except Exception as e:
            return LLMResponse(
                success=False,
                error=str(e)
            )

    def embed(self, text):
        try:
            response = self.client.embeddings.create(
                model=settings.OPENAI_EMBEDDING_MODEL,
                input=text
            )

            return EmbeddingResponse(
                success=True,
                embedding=response.data[0].embedding
            )

        except Exception as e:
            return EmbeddingResponse(
                success=False,
                error=str(e)
            )


LLMRegistry.register("openai", OpenAIProvider)