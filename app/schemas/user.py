from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    full_name: Optional[str] = None
    email: EmailStr
    is_admin: Optional[bool] = None

    # Pydantic v2: enable attribute-based validation for ORM objects
    model_config = {"from_attributes": True}
