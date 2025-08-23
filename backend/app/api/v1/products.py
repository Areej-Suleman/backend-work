print("✅ products.py loaded")
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import ProductSchema
from app.core.db import get_db
from app.crud import product as crud_product
from app.schemas.product import ProductSchema

router = APIRouter()

@router.get("/", response_model=List[ProductSchema])
def list_products(db: Session = Depends(get_db)):
    return crud_product.get_all(db)

@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud_product.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product