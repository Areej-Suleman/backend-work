from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app import crud, schemas
router = APIRouter()

@router.get("/")
def list_brands(db: Session = Depends(get_db)):
    return crud.brand.get_all(db)

@router.get("/{brand_id}")
def get_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = crud.brand.get_by_id(db, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand