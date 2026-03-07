from app.db.repositories.chat_document_repo import ChatDocumentRepository
from app.db.repositories.chat_document_chunk_repo import ChatDocumentChunkRepository
from app.modules.embedding.pdf.processor import PDFProcessor
from app.modules.ingestion.pipeline.ingestion_pipeline import IngestionPipeline
from app.modules.embedding.text_chunker import TextChunker
from app.modules.embedding.embedder import Embedder
from uuid import UUID


class EmbeddingService:

    @staticmethod
    async def process_document(cd_id: UUID):
        try:
            document = await ChatDocumentRepository.get_by_id_sync(cd_id)
            if not document:
                await ChatDocumentRepository.update_status(cd_id, "failed", "Document not found")
                return
            
            await ChatDocumentRepository.update_status(cd_id, "processing", None)
            

            # 2️. Extract PDF text
            print("Extracting PDF text.......")
            chunks = PDFProcessor().process(document.file_path)
            # chunks = IngestionPipeline().run(document.file_path)
            print("chunks length", len(chunks))

            # 3. Generate embeddings
            print("Generate embeddings................")
            vectors = Embedder().embed_batch([c["text"] for c in chunks])
            print("vectors length", len(vectors))

            # 4. Insert into chat_document_chunks
            await ChatDocumentChunkRepository.bulk_insert(
                cd_id=cd_id,
                cs_id=document.cs_id,
                chunks=chunks,
                embeddings=vectors
            )

            # 5. Update status
            await ChatDocumentRepository.update_status(cd_id, "indexed", None)

        except Exception as e:
            print("exception", e)
            await ChatDocumentRepository.update_status(cd_id, "failed", str(e))
