# llm/providers/gemini_provider.py
from google import genai
from google.genai.types import GenerateContentConfig, EmbedContentConfig
from app.core.llm.provider.batch_builder import BatchBuilder
from app.core.llm.provider.rate_limiter import RateLimiter
from config import settings
from app.core.llm.base import BaseLLM
from app.core.llm.schemas import LLMResponse, EmbeddingResponse
from app.core.llm.registry import LLMRegistry
from typing import List
import asyncio
import time

EMBEDDING_FILE = "cached_embeddings.json"

class GeminiProvider(BaseLLM):

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )
        self.embedding_model = settings.GEMINI_EMBEDDING_MODEL
        self.batch_builder = BatchBuilder()
        self.rate_limiter = RateLimiter()

    async def generate(self, system_prompt, user_prompt, temperature=0.2) -> LLMResponse:
        print("Generating with GeminiProvider.......")
        try:
        
            # prompt = f"{system_prompt}\n\n{user_prompt}"

            result = await self.client.aio.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=user_prompt,
                config=GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=temperature
                    )
            )

            print("Text:", result.text)
            tokens_used = 0
            if result.usage_metadata:
                tokens_used = result.usage_metadata.total_token_count

            return LLMResponse(
                success=True,
                content=result.text,
                tokens_used=tokens_used
            )

        except Exception as e:
            error_str = str(e)
            print("gemini exception:", error_str)

            # Handle quota exceeded
            if "RESOURCE_EXHAUSTED" in error_str or "429" in error_str:
                return LLMResponse(
                    success=False,
                    error="Gemini API quota exceeded. Please try again later.",
                    
                )

            # Handle rate limit
            if "rate limit" in error_str.lower():
                return LLMResponse(
                    success=False,
                    error="Too many requests. Please wait a moment and try again."
                )

            # Generic fallback
            return LLMResponse(
                success=False,
                error="LLM service temporarily unavailable."
            )

    async def embed_text(self, text:str) -> EmbeddingResponse:
        try:
            result = await self.client.aio.models.embed_content(
                model=settings.GEMINI_EMBEDDING_MODEL,
                contents=text,
                config = EmbedContentConfig(
                    task_type="QUESTION_ANSWERING",
                    output_dimensionality=1536
                )
            )
            embedding_vector = [e.values for e in result.embeddings]

            return EmbeddingResponse(
                success=True,
                embedding=embedding_vector[0]
            )

        except Exception as e:
            return EmbeddingResponse(
                success=False,
                error=str(e)
            )
        
    async def embed_batch(self, texts:List[str]) -> EmbeddingResponse:
            
        print("Embedding batch with GeminiProvider......")
        batches = self.batch_builder.build(texts)
        print("batches lenght", len(batches))

        all_embeddings: List[List[float]] = []
        print("batche builds successfully.......")

        retry_attempts = 5
        delay = 1 

        try:
            for batch in batches:
                if len(batch) > 100:
                    raise ValueError("Gemini batch limit exceeded")

                await self.rate_limiter.wait_if_needed()

                try: 
                    response  = await self.client.aio.models.embed_content(
                        model=self.embedding_model,
                        contents=batch,
                        config = EmbedContentConfig(
                            task_type="QUESTION_ANSWERING",
                            output_dimensionality=1536
                        )
                    )
            
                    embeddings = [e.values for e in response.embeddings]
                    all_embeddings.extend(embeddings) 
                    await asyncio.sleep(0.5)

                except Exception as e:
                    if "429 Too Many Requests" in str(e):
                        if retry_attempts > 0:
                            retry_attempts -= 1
                            print(f"Rate limit exceeded, retrying after {delay} seconds...")
                            await asyncio.sleep(delay)
                            delay *= 2  
                            continue
                        else:
                            raise

                    if "429 RESOURCE_EXHAUSTED" in str(e):
                        retry_attempts -= 1
                        if retry_attempts > 0:
                            await asyncio.sleep(delay)
                            delay *= 2  # Exponential backoff
                            continue  # Retry with the new API key
                        else:
                            raise


                    else:
                        raise                                                        

            print("embedding length", len(all_embeddings))

            return EmbeddingResponse(
                success=True,
                embedding=all_embeddings
            )

        except Exception as e:
            return EmbeddingResponse(
                success=False,
                error=str(e)
            )


LLMRegistry.register("gemini", GeminiProvider)