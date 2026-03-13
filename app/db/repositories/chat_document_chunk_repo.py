from typing import List, Dict
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, text
from app.db.models.chat_document_chunk import ChatDocumentChunk
from app.core.session_manager import use_db_async
from pgvector.sqlalchemy import Vector


class ChatDocumentChunkRepository:

    @staticmethod
    @use_db_async
    async def bulk_insert(
        cd_id: UUID,
        cs_id: UUID,
        chunks: List[Dict],
        embeddings: List[List[float]],
        db: AsyncSession
    ) -> None:
        """
        Bulk insert document chunks with embeddings.
        Optimized for large batch insert.
        """

        if len(chunks) != len(embeddings):
            raise ValueError("Chunks and embeddings length mismatch")

        try:
            records = []

            for chunk, emb in zip(chunks, embeddings):
                

                # Optional: sanity check for dimension
                if len(emb) != 1536:
                    raise ValueError(
                        f"Embedding dimension mismatch for chunk {chunk['chunk_index']}: {len(emb)}"
                    )
            
                records.append({
                    "cd_id": cd_id,
                    "cs_id": cs_id,
                    "chunk_index": chunk["chunk_index"],
                    "content": chunk["content"],
                    "page_number": chunk["metadata"].get("page"),
                    "keywords": chunk["metadata"].get("keywords"),
                    "meta": chunk["metadata"].get("meta"),
                    "embedding": emb,
                })

            stmt = insert(ChatDocumentChunk).values(records)

            await db.execute(stmt)
            await db.commit()

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    @use_db_async
    async def search_similar(
        cs_id: UUID,
        query_embedding: List[float],
        query_text: str,
        top_k: int = 5,
        score_threshold: float = 0.7,
        db: AsyncSession = None
    ) -> List[ChatDocumentChunk]:
        """
        Perform cosine similarity search using pgvector.
        """

        try:
            # sql = text("""
            #     SELECT *,
            #            1 - (embedding <=> :embedding) AS score
            #     FROM chat_document_chunks
            #     WHERE cs_id = :cs_id
            #       AND 1 - (embedding <=> :embedding) >= :score_threshold
            #     ORDER BY score DESC
            #     LIMIT :top_k
            # """)

            sql = text("""
            SELECT
                cdc_id,
                cd_id,
                cs_id,
                chunk_index,
                content,
                embedding,
                page_number,
                keywords,
                meta,
                created_at,

                (
                    0.65 * (1 - (embedding <=> :embedding)) +
                    0.25 * ts_rank(content_tsv, plainto_tsquery('english', :query)) +
                    0.10 * CASE
                        WHEN keywords && string_to_array(:query, ' ')
                        THEN 1
                        ELSE 0
                    END
                ) AS score

            FROM chat_document_chunks

            WHERE cs_id = :cs_id

            ORDER BY score DESC

            LIMIT :top_k
            """)


            result = await db.execute(
                sql,
                {
                    "cs_id": cs_id,
                    "embedding": query_embedding,
                    "top_k": top_k,
                    "query": query_text,
                    "score_threshold": score_threshold
                }
            )

            rows = result.fetchall()
            print("rows", rows)

            # return [
            #     ChatDocumentChunk(**row._mapping)
            #     for row in rows
            # ]

            return [
                ChatDocumentChunk(
                    cdc_id=row._mapping['cdc_id'],
                    cd_id=row._mapping['cd_id'],
                    cs_id=row._mapping['cs_id'],
                    chunk_index=row._mapping['chunk_index'],
                    content=row._mapping['content'],
                    embedding=row._mapping['embedding'],
                    page_number=row._mapping['page_number'],
                    created_at=row._mapping['created_at']
                )
                for row in rows
            ]

        except Exception as e:
            raise e
