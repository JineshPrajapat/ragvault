from app.db.repositories.chat_document_repo import ChatDocumentRepository
from app.db.repositories.chat_document_chunk_repo import ChatDocumentChunkRepository
from app.modules.rag_ingestion.pipeline.ingestion_pipeline import IngestionPipeline
from app.core.llm.service import LLMService
from uuid import UUID

class EmbeddingService:

    @staticmethod
    async def process_document(cd_id: UUID):
        print(f"EmbeddingService.process_document: {cd_id}")
        try:
            document = await ChatDocumentRepository.get_by_id_sync(cd_id)
            if not document:
                await ChatDocumentRepository.update_status(cd_id, "failed", "Document not found")
                return
            
            await ChatDocumentRepository.update_status(cd_id, "processing", None)
            

            # 2️. Extract PDF text
            print("Extracting PDF text.......")
            parsed = IngestionPipeline().run(document.file_path)
            chunks = parsed["text"]

            # 3. Generate embeddings
            print("Generate embeddings................")
            llm_service = LLMService("gemini")
            embedding_result = await llm_service.embed_batch([c["content"] for c in chunks])
            # print("\n\nembedding_result\n\n", embedding_result)

            if not embedding_result.success:
                return {"error": embedding_result.error}                    #update status
            
            for i, emb in enumerate(embedding_result.embedding):
                if len(emb) != 1536:
                    raise ValueError(
                        f"Embedding length mismatch in batch {i}, index {i}: got {len(emb)}"    #update status
                    )
            
            # 4. Insert into chat_document_chunks
            print("\n\nbulk_insert\n\n")
            await ChatDocumentChunkRepository.bulk_insert(
                cd_id=cd_id,
                cs_id=document.cs_id,
                chunks=chunks,
                embeddings=embedding_result.embedding
            )

            # 5. Update status
            await ChatDocumentRepository.update_status(cd_id, "indexed", None)

        except Exception as e:
            print("exception", e)
            await ChatDocumentRepository.update_status(cd_id, "failed", str(e))
