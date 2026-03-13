from typing import Any, Optional, TypeVar, Generic
from pydantic import BaseModel


class APIResponse(BaseModel):
    status: str
    status_code: int
    message: str
    data: Optional[Any] = None

T = TypeVar("T")

class AppServiceResult(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
