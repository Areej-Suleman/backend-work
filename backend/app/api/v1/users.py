from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.core.db import get_db
from app import crud, schemas
router = APIRouter()

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.users.create_user(db, user)

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.users.get_user(db, user_id)
