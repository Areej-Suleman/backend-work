from pydantic import BaseModel
from typing import Optional

class BrandBase(BaseModel):
    name: str
    country: Optional[str] = None
    website_url: Optional[str] = None
    image_url: Optional[str] = None
    is_international: bool = True

class BrandCreate(BrandBase):
    pass

class BrandResponse(BrandBase):
    id: int
    
    class Config:
        from_attributes = True
