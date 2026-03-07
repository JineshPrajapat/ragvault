# # llm/providers/gemini_provider.py
# import google.generativeai as genai
# from config import settings
# from app.core.llm.base import BaseLLM
# from app.core.llm.schemas import LLMResponse, EmbeddingResponse
# from llm.registry import LLMRegistry


# class GeminiProvider(BaseLLM):

#     def __init__(self):
#         genai.configure(api_key=settings.GEMINI_API_KEY)
#         self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

#     def generate(self, system_prompt, user_prompt, temperature=0.2):
#         try:
#             prompt = f"{system_prompt}\n\n{user_prompt}"

#             response = self.model.generate_content(
#                 prompt,
#                 generation_config={"temperature": temperature}
#             )

#             return LLMResponse(
#                 success=True,
#                 content=response.text
#             )

#         except Exception as e:
#             return LLMResponse(
#                 success=False,
#                 error=str(e)
#             )

#     def embed(self, text):
#         try:
#             response = genai.embed_content(
#                 model=settings.GEMINI_EMBEDDING_MODEL,
#                 content=text
#             )

#             return EmbeddingResponse(
#                 success=True,
#                 embedding=response["embedding"]
#             )

#         except Exception as e:
#             return EmbeddingResponse(
#                 success=False,
#                 error=str(e)
#             )


# LLMRegistry.register("gemini", GeminiProvider)