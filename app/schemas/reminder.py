# app/schemas/reminder.py

from typing import Optional
from pydantic import BaseModel
from datetime import time

# Schemas aligned with app/models/reminder.py

class ReminderBase(BaseModel):
    title: str
    description: Optional[str] = None
    reminder_type: Optional[str] = None  # morning_routine, evening_routine, weekly, etc.
    reminder_time: Optional[time] = None
    frequency: Optional[str] = None  # daily, weekly, monthly
    is_active: Optional[bool] = True

class ReminderCreate(ReminderBase):
    user_id: int
    product_id: int

class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    reminder_type: Optional[str] = None
    reminder_time: Optional[time] = None
    frequency: Optional[str] = None
    is_active: Optional[bool] = None

class Reminder(ReminderBase):
    id: int
    user_id: int
    product_id: int

    class Config:
        from_attributes = True  # Pydantic v2 compatibility
