from uuid import UUID
from typing import List
from app.db.repositories.chat_document_chunk_repo import ChatDocumentChunkRepository
from app.core.llm.service import LLMService
from app.schemas.api_response import AppServiceResult


class RetrievalService:
    MAX_CONTEXT_LENGTH = 8000

    @staticmethod
    async def retrieve_context(
        cs_id: UUID,
        question: str,
        top_k: int = 5
    ) -> AppServiceResult[dict]:
        """
        1️⃣ Embed query
        2️⃣ Retrieve top-k chunks
        3️⃣ Build context string
        """
        try:
            if not question or not question.strip():
                return AppServiceResult(success=False, error="Question cannot be empty")
            
            # 1️⃣ Embed query
            llm_service = LLMService("gemini")
            query_embedding = await llm_service.embed_text(text=question)

            if not query_embedding.success:
                return AppServiceResult(success=False, error=query_embedding.error)

            # Do NOT convert to string! Pass as list of floats
            embedding_str = "[" + ",".join(map(str, query_embedding.embedding)) + "]"

            # 2️⃣ Vector search
            chunks = await ChatDocumentChunkRepository.search_similar(
                cs_id=cs_id,
                query_embedding=embedding_str,
                top_k=top_k,
                query_text=question
            )

            if not chunks:
                return AppServiceResult(success=False, error="No relevant chunks found")

            # 3️⃣ Build context
            context_parts: List[str] = []

            chunks = sorted(chunks, key=lambda x: x.page_number or 0)

            for chunk in chunks:
                if chunk.content:
                    context_parts.append( f"\n{chunk.content.strip()}")
            
            if not context_parts:
                return AppServiceResult(success=False, error="Chunks were empty")
            
            context = "\n\n---\n\n".join(context_parts)
            
            if len(context) > RetrievalService.MAX_CONTEXT_LENGTH:
                context = context[:RetrievalService.MAX_CONTEXT_LENGTH]

            return AppServiceResult(success=True, data=context)

        except Exception as e:
            print("Error in retrieve_context:", str(e))
            return AppServiceResult(success=False, error="Context retrieval failed")