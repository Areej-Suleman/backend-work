from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app import crud, schemas

router = APIRouter()

@router.get("/users")
def list_all_users(db: Session = Depends(get_db)):
    return crud.users.get_all(db)

@router.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.users.delete(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}