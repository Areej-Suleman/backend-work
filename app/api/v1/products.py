print("✅ products.py loaded")
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.product import ProductUpdate
from app.schemas.product import ProductCreate
from app.schemas.product import ProductSchema
from app.core.db import get_db
from app.crud import product as crud_product
from app.core.permissions import require_admin, get_optional_user, Permissions, require_permission

router = APIRouter()

@router.get("/", response_model=List[ProductSchema])
def list_products(
    db: Session = Depends(get_db),
    current_user = Depends(get_optional_user)  # Optional - public endpoint but can show different data for logged users
):
    """List all products - Public endpoint with optional authentication"""
    products = crud_product.get_all(db)
    # Could add user-specific features here if authenticated
    return products

# Place static routes before dynamic ones to avoid matching conflicts
@router.get("/search")
def search_products(
    q: str = None,
    category: str = None,
    brand_id: int = None,
    min_price: float = None,
    max_price: float = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_optional_user)  # Optional authentication
):
    """Search products - Public endpoint with optional authentication"""
    return crud_product.search_products(db, q, category, brand_id, min_price, max_price)

@router.get("/{product_id}", response_model=ProductSchema)
def get_product(
    product_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_optional_user)  # Optional authentication
):
    """Get product by ID - Public endpoint"""
    product = crud_product.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductSchema)
def create_product(
    product: ProductCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(require_permission(Permissions.MANAGE_PRODUCTS))  # Admin only
):
    """Create new product - Admin only"""
    return crud_product.create(db, product)

@router.put("/{product_id}", response_model=ProductSchema)
def update_product(
    product_id: int, 
    product: ProductUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(require_permission(Permissions.MANAGE_PRODUCTS))  # Admin only
):
    """Update product - Admin only"""
    return crud_product.update(db, product_id, product)

@router.delete("/{product_id}")
def delete_product(
    product_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(require_permission(Permissions.DELETE_ANY_CONTENT))  # Admin only
):
    """Delete product - Admin only"""
    crud_product.delete(db, product_id)
    return {"message": "Product deleted successfully"}
