from fastapi import HTTPException, UploadFile
from uuid import UUID
from app.db.repositories.chat_session_repo import ChatSessionRepository
from app.db.repositories.chat_document_repo import ChatDocumentRepository
from app.core.storage import LocalStorage
from app.utils.hashing import calculate_file_hash
from app.tasks.document_tasks import process_document


class ChatDocumentService:

    @staticmethod
    async def upload_document(u_id: UUID, cs_id: UUID, file: UploadFile):

        session = await ChatSessionRepository.get_by_id(cs_id)

        if not session or session.u_id != u_id or session.status != "active":
            raise HTTPException(status_code=404, detail="Invalid session")

        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF allowed")

        content = await file.read()

        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty PDF")
        
        if len(content) > 20 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large")
        
        file_hash = calculate_file_hash(content)

        storage = LocalStorage()
        file_path, file_size = await storage.save(content, file.filename)

        document = await ChatDocumentRepository.create({
            "cs_id": cs_id,
            "file_name": file.filename,
            "file_path": file_path,
            "file_hash": file_hash,
            "file_size": file_size,
            "storage_type": "local",
            "processing_status": "uploaded"
        })

        print('triggered celery')

        # TODO: Trigger background embedding task
        process_document.delay(str(document.cd_id))
        

        return document
    

    @staticmethod
    async def list_documents_by_session(u_id: UUID, cs_id: UUID):
        return await ChatDocumentRepository.list_by_session(cs_id=cs_id)
