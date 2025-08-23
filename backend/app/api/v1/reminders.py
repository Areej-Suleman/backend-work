from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app import crud, schemas
router = APIRouter()

@router.post("/")
def create_reminder(reminder: schemas.ReminderCreate, db: Session = Depends(get_db)):
    return crud.reminders.create(db, reminder)

@router.get("/{user_id}")
def get_reminders(user_id: int, db: Session = Depends(get_db)):
    return crud.reminders.get_for_user(db, user_id)