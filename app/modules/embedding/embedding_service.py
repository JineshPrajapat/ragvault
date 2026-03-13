from app.db.repositories.chat_document_repo import ChatDocumentRepository
from app.db.repositories.chat_document_chunk_repo import ChatDocumentChunkRepository
from app.modules.rag_ingestion.pipeline.ingestion_pipeline import IngestionPipeline
from app.core.llm.service import LLMService
from uuid import UUID
import time

class EmbeddingService:

    def __init__(self, llm_provider: str = "gemini"):
        self.llm_service = LLMService(llm_provider)
        self.pipeline = IngestionPipeline()

    async def process_document(self,cd_id: UUID):

        start_time = time.perf_counter()
        print(f"[*] Starting Ingestion Pipeline for Document: {cd_id}")

        try:
            print(f"[1/4] INITIALIZING | Fetching document metadata...")
            document = await ChatDocumentRepository.get_by_id_sync(cd_id)

            if not document:
                print(f"[!] FAILED | Document {cd_id} not found in database.")
                await ChatDocumentRepository.update_status(cd_id, "failed", "Document not found")
                return
            
            await ChatDocumentRepository.update_status(cd_id, "processing", None)
            

            # 2️. Extract PDF text
            print(f"[2/4] EXTRACTION | Parsing PDF: {document.file_path}")
            parsed = self.pipeline.run(document.file_path)
            chunks = parsed.get("text", [])

            if not chunks:
                raise ValueError("No text content could be extracted from the document.")

            print(f"[+] COMPLETED | Extracted {len(chunks)} chunks.")

            # 3. Generate embeddings
            print(f"[3/4] EMBEDDING | Generating vectors via Gemini...")
            contents = [c["content"] for c in chunks]
            embedding_result = await self.llm_service.embed_batch(contents)

            if not embedding_result.success:
                raise Exception(f"LLM Embedding Error: {embedding_result.error}")                    #update status
            
            # 4. Insert into chat_document_chunks
            print(f"[4/4] PERSISTENCE | Bulk inserting {len(chunks)} vectors into DB...")
            await ChatDocumentChunkRepository.bulk_insert(
                cd_id=cd_id,
                cs_id=document.cs_id,
                chunks=chunks,
                embeddings=embedding_result.embedding
            )

            # 5. Update status
            await ChatDocumentRepository.update_status(cd_id, "indexed", None)

            total_time = time.perf_counter() - start_time
            print(f"[*] SUCCESS | Document {cd_id} indexed in {total_time:.2f}s")

        except Exception as e:
            print("[CRITICAL] Ingestion Error", str(e))
            await ChatDocumentRepository.update_status(cd_id, "failed", str(e))
            return
