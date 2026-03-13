from dataclasses import dataclass
from typing import Optional, List


@dataclass
class LLMResponse:
    success: bool
    content: Optional[str] = None
    tokens_used: Optional[int] = None
    error: Optional[str] = None
    error_code: Optional[str] = None


@dataclass
class EmbeddingResponse:
    success: bool
    embedding: Optional[List[float]] = None
    error: Optional[str] = None