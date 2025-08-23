# app/schemas/reminder.py

from pydantic import BaseModel
from datetime import datetime

class ReminderCreate(BaseModel):
    title: str
    description: str
    remind_at: datetime