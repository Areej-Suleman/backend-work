from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.core.db import get_db
from app import crud, schemas
from app.core.config import settings

# OAuth2 bearer token for Swagger Authorize button
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def require_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """Allow only admin users or the configured ADMIN_EMAIL."""
    user = crud.users.get_current_user(db, token)
    is_admin_flag = bool(getattr(user, "is_admin", False))
    is_configured_admin = bool(settings.ADMIN_EMAIL and user.email == settings.ADMIN_EMAIL)
    if not (is_admin_flag or is_configured_admin):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")
    return user

# Apply the admin dependency to all routes in this router
router = APIRouter(dependencies=[Depends(require_admin)])

@router.get("/users")
def list_all_users(db: Session = Depends(get_db)):
    return crud.users.get_all(db)

@router.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud.users.delete_user(db, user_id)
    return {"detail": "User deleted"}

@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db)):
    return {
        "total_users": crud.users.count_all(db),
        "total_products": crud.product.count_all(db),
        "total_brands": crud.brand.count_all(db),
        "total_analyses": crud.analysis.count_all(db),
        "recent_signups": crud.users.get_recent_signups(db, days=7)
    }

@router.get("/products")
def list_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.product.get_all(db, skip=skip, limit=limit)

@router.post("/products")
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.product.create(db, product)

@router.put("/products/{product_id}")
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return crud.product.update(db, product_id, product)

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = crud.product.delete(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}

@router.get("/brands")
def list_all_brands(db: Session = Depends(get_db)):
    return crud.brand.get_all(db)

@router.post("/brands")
def create_brand_admin(brand: schemas.BrandCreate, db: Session = Depends(get_db)):
    return crud.brand.create(db, brand)

@router.get("/analyses")
def list_all_analyses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.analysis.get_all(db, skip=skip, limit=limit)

@router.get("/users/{user_id}/activity")
def get_user_activity(user_id: int, db: Session = Depends(get_db)):
    return {
        "analyses": crud.analysis.get_user_analyses(db, user_id),
        "reminders": crud.reminders.get_for_user(db, user_id),
        "chat_logs": crud.chat.get_user_chat_history(db, user_id)
    }
