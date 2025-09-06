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

@router.post("/", response_model=schemas.BrandResponse)
def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db)):
    return crud.brand.create(db, brand)

@router.put("/{brand_id}", response_model=schemas.BrandUpdate)
def update_brand(brand_id: int, brand: schemas.BrandUpdate, db: Session = Depends(get_db)):
    db_brand = crud.brand.get_by_id(db, brand_id)
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return crud.brand.update(db, brand_id, brand)

@router.delete("/{brand_id}")
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    success = crud.brand.delete(db, brand_id)
    if not success:
        raise HTTPException(status_code=404, detail="Brand not found")
    return {"detail": "Brand deleted successfully"}

@router.get("/{brand_id}/products")
def get_brand_products(brand_id: int, db: Session = Depends(get_db)):
    brand = crud.brand.get_by_id(db, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return crud.product.get_by_brand(db, brand_id)

@router.post("/{brand_id}/images")
def add_brand_image(brand_id: int, image_data: schemas.BrandImageCreate, db: Session = Depends(get_db)):
    brand = crud.brand.get_by_id(db, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return crud.brand.add_image(db, brand_id, image_data)
