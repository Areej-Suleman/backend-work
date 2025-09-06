from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    user_id: int
    text: str

class SkincareAdviceRequest(BaseModel):
    user_id: int
    skin_type: Optional[str] = None  # "oily", "dry", etc.
    concerns: List[str] = []
    age: Optional[int] = None
    budget: Optional[float] = None
