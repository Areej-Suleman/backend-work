from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app import crud, schemas
router = APIRouter()

@router.put("/{user_id}")
def update_profile(user_id: int, profile: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.users.update_user(db, user_id, profile)