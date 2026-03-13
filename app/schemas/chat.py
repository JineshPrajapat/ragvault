from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str
    
class RenameSessionRequest(BaseModel):
    title: str
