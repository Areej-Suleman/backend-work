from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate
from app.core.db import get_db
from app import crud, schemas
from fastapi.security import OAuth2PasswordBearer
from app.core.permissions import (
    get_current_authenticated_user, 
    require_admin, 
    require_owner_or_admin,
    Permissions,
    require_permission
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
router = APIRouter()

@router.get("/me", response_model=schemas.UserResponse)
def get_current_user(
    current_user = Depends(get_current_authenticated_user),
    db: Session = Depends(get_db)
):
    """Get current authenticated user profile - User/Admin access"""
    return schemas.UserResponse.from_orm(current_user)

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register new user - Public endpoint"""
    return crud.users.create_user(db, user)

@router.get("/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_owner_or_admin)  # ✅ fixed
):
    """Get user by ID - Owner or Admin access only"""
    return crud.users.get_user(db, user_id)

@router.put("/{user_id}")
def update_user(
    user_id: int, 
    user_update: schemas.UserUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(require_owner_or_admin)  # ✅ fixed
):
    """Update user - Owner or Admin access only"""
    return crud.users.update_user(db, user_id, user_update)

@router.delete("/{user_id}")
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(require_permission(Permissions.MANAGE_USERS))  # Admin only
):
    """Delete user - Admin only"""
    crud.users.delete_user(db, user_id)
    return {"message": "User deleted successfully"}

@router.get("/{user_id}/preferences")
def get_user_preferences(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(require_owner_or_admin)  # ✅ fixed
):
    """Get user preferences - Owner or Admin access only"""
    return crud.users.get_user_preferences(db, user_id)
