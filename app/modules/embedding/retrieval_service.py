from uuid import UUID
from typing import List
from app.modules.embedding.embedder import Embedder
from app.db.repositories.chat_document_chunk_repo import ChatDocumentChunkRepository
import traceback


class RetrievalService:

    @staticmethod
    async def retrieve_context(
        cs_id: UUID,
        question: str,
        top_k: int = 10
    ) -> str:
        """
        1️⃣ Embed query
        2️⃣ Retrieve top-k chunks
        3️⃣ Build context string
        """
        try:
            # 1️⃣ Embed query
            query_embedding = Embedder().embed_text(text=question)
            print("query_embedding length:", len(query_embedding))
            print("query_embedding sample:", query_embedding[:5])  # first 5 floats

            # Do NOT convert to string! Pass as list of floats
            embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

            # 2️⃣ Vector search
            chunks = await ChatDocumentChunkRepository.search_similar(
                cs_id=cs_id,
                query_embedding=embedding_str,
                top_k=top_k,
                query_text=question
            )

            if not chunks:
                print("No chunks returned from search_similar")
                return ""

            # 3️⃣ Build context
            context_parts: List[str] = []

            chunks = sorted(chunks, key=lambda x: x.page_number or 0)

            for chunk in chunks:
                context_parts.append(
                    f"[Page {chunk.page_number}]\n{chunk.content}"
                )

            return "\n\n---\n\n".join(context_parts)

        except Exception as e:
            print("Error in retrieve_context:", str(e))
            traceback.print_exc()
            return ""