from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChatMessage(BaseModel):
    id: int
    user_id: int
    message: str
    timestamp: Optional[datetime] = None

    class Config:
        orm_mode = True