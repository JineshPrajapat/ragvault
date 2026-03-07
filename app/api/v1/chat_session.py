from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from uuid import UUID
from app.modules.chat_session.chat_session_service import ChatSessionService
from app.modules.chat.chat_message_service import ChatMessageService
from app.modules.chat_document.chat_document_service import ChatDocumentService
from app.modules.chat.chat_service import ChatService
from app.schemas.chat_session import ChatSessionCreate
from app.utils.response_builder import ResponseBuilder
from app.schemas.api_response import APIResponse
from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str
    
class RenameSessionRequest(BaseModel):
    title: str

router = APIRouter(tags=["Chat Sessions"])


@router.post("", response_model=APIResponse)
async def create_session(payload: ChatSessionCreate, req: Request):
    user_id = req.state.user_id

    session = await ChatSessionService.create_session(
        u_id=user_id,
        title=payload.title
    )

    return ResponseBuilder.success(session, "Session created successfully")

@router.patch("/{cs_id}")
async def rename_session(cs_id: UUID, payload: RenameSessionRequest):
    await ChatSessionService.rename_session(cs_id, payload.title)
    return ResponseBuilder.success(None, "Session renamed successfully")

@router.get("", response_model=APIResponse)
async def list_sessions(req: Request):
    user_id = req.state.user_id

    sessions = await ChatSessionService.list_sessions(user_id)

    return ResponseBuilder.success(sessions)


@router.get("/{cs_id}", response_model=APIResponse)
async def get_session(cs_id: UUID, req: Request):
    user_id = req.state.user_id

    session = await ChatSessionService.get_session(user_id, cs_id)

    return ResponseBuilder.success(session)


@router.delete("/{cs_id}", response_model=APIResponse)
async def delete_session(cs_id: UUID, req: Request):
    user_id = req.state.user_id

    await ChatSessionService.delete_session(user_id, cs_id)

    return ResponseBuilder.success(None, "Session deleted successfully")


@router.post("/{cs_id}/upload", response_model=APIResponse)
async def upload_document(cs_id: UUID, file: UploadFile = File(...), req: Request = None):
    user_id = req.state.user_id
    try:
        document = await ChatDocumentService.upload_document(
            u_id=user_id,
            cs_id=cs_id,
            file=file
        )

        return ResponseBuilder.success(document, "Document uploaded successfully")

    except ValueError as e:
        return ResponseBuilder.error(message=str(e), code=400)


@router.get("/{cs_id}/documents", response_model=APIResponse)
async def list_documents(cs_id: UUID, req: Request):
    user_id = req.state.user_id

    documents = await ChatDocumentService.list_documents_by_session(user_id, cs_id)

    return ResponseBuilder.success(documents, "Document list retriewd successfully")


@router.post("/{cs_id}/ask", response_model=APIResponse)
async def ask_question(cs_id: UUID, payload: AskRequest):

    result = await ChatService.ask_question(
        cs_id=cs_id,
        question=payload.question,
    )

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return ResponseBuilder.success(result, "rag result successfully")


@router.get("/{cs_id}/messages", response_model=APIResponse)
async def get_messages(
    cs_id: UUID,
    offset: int = 0,
    limit: int = 50
):
    messages = await ChatMessageService.get_messages(
        cs_id=cs_id,
        offset=offset,
        limit=limit
    )
    return ResponseBuilder.success(messages, "Messages retrieved successfully")