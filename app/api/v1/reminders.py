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

@router.put("/{reminder_id}", response_model=schemas.Reminder)
def update_reminder(reminder_id: int, reminder: schemas.ReminderUpdate, db: Session = Depends(get_db)):
    db_reminder = crud.reminders.get_by_id(db, reminder_id)
    if not db_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return crud.reminders.update(db, reminder_id, reminder)

@router.delete("/{reminder_id}")
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    success = crud.reminders.delete(db, reminder_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return {"detail": "Reminder deleted successfully"}

@router.get("/")
def get_all_reminders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.reminders.get_all(db, skip=skip, limit=limit)

@router.post("/{reminder_id}/complete")
def mark_reminder_complete(reminder_id: int, db: Session = Depends(get_db)):
    reminder = crud.reminders.get_by_id(db, reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return crud.reminders.mark_complete(db, reminder_id)

@router.get("/upcoming/{user_id}")
def get_upcoming_reminders(user_id: int, days: int = 7, db: Session = Depends(get_db)):
    return crud.reminders.get_upcoming(db, user_id, days)
