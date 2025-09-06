from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ResponseBase(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 100

class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    skip: int
    limit: int
    has_more: bool

class FileUploadResponse(BaseModel):
    filename: str
    file_path: str
    file_size: int
    content_type: str
    uploaded_at: datetime

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int
