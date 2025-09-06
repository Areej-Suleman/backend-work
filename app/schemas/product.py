from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProductImage(BaseModel):
    id: int
    image_url: str
    is_primary: bool
    created_at: Optional[datetime]

    class Config:
        from_attributes = True  # Updated from orm_mode to from_attributes for Pydantic v2

class ProductCreate(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    brand_id: int
    user_id: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    brand_id: Optional[int] = None

class ProductSchema(BaseModel):  # This is imported as ProductSchema in your API
    id: int
    name: str
    category: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    brand_id: int
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    images: List[ProductImage] = []  # No Optional here; empty list by default

    class Config:
        from_attributes = True  # Updated from orm_mode to from_attributes for Pydantic v2
