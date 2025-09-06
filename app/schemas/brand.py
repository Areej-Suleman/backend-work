from pydantic import BaseModel
from typing import Optional

class BrandBase(BaseModel):
    name: str
    description: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None  # align with SQLAlchemy model
    is_international: bool = True

class BrandCreate(BrandBase):
    user_id: int  # required by the Brand model (non-nullable)

class BrandResponse(BrandBase):
    id: int
    
    class Config:
        from_attributes = True

class BrandUpdate(BrandBase):
    pass

class BrandImageCreate(BaseModel):
    image_url: str
    is_primary: bool = False
