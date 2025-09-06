from datetime import datetime, date, timedelta, time as dtime
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.reminder import Reminder


def create(db: Session, payload) -> Reminder:
    data = payload.dict() if hasattr(payload, "dict") else dict(payload)
    rem = Reminder(**data)
    db.add(rem)
    db.commit()
    db.refresh(rem)
    return rem


def get_for_user(db: Session, user_id: int) -> List[Reminder]:
    return db.query(Reminder).filter(Reminder.user_id == user_id).order_by(Reminder.created_at.desc()).all()


def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Reminder]:
    return db.query(Reminder).order_by(Reminder.created_at.desc()).offset(skip).limit(limit).all()


def get_by_id(db: Session, reminder_id: int) -> Optional[Reminder]:
    return db.query(Reminder).filter(Reminder.id == reminder_id).first()


def update(db: Session, reminder_id: int, payload) -> Optional[Reminder]:
    rem = get_by_id(db, reminder_id)
    if not rem:
        return None
    changes = payload.dict(exclude_unset=True) if hasattr(payload, "dict") else dict(payload or {})
    for k, v in changes.items():
        setattr(rem, k, v)
    db.commit()
    db.refresh(rem)
    return rem


def delete(db: Session, reminder_id: int) -> bool:
    rem = get_by_id(db, reminder_id)
    if not rem:
        return False
    db.delete(rem)
    db.commit()
    return True


def mark_complete(db: Session, reminder_id: int) -> Optional[Reminder]:
    rem = get_by_id(db, reminder_id)
    if not rem:
        return None
    rem.is_active = False
    db.add(rem)
    db.commit()
    db.refresh(rem)
    return rem


def get_upcoming(db: Session, user_id: int, days: int = 7) -> List[dict]:
    """Return active reminders with a computed next_occurrence within the window.
    Simplified schedule: uses reminder_time and frequency strings.
    """
    now = datetime.now()
    window_end = now + timedelta(days=days)

    items = db.query(Reminder).filter(Reminder.user_id == user_id, Reminder.is_active == True).all()
    upcoming: List[dict] = []
    for rem in items:
        # Default next occurrence: today at reminder_time
        rt: Optional[dtime] = rem.reminder_time
        if rt is None:
            next_dt = now
        else:
            today_dt = datetime.combine(date.today(), rt)
            next_dt = today_dt if today_dt >= now else today_dt + timedelta(days=1)

        freq = (rem.frequency or "daily").lower()
        if freq == "weekly" and next_dt < now + timedelta(days=1):
            next_dt = next_dt + timedelta(days=7)
        elif freq == "monthly":
            # naive monthly: add 30 days if today has passed
            if next_dt < now:
                next_dt = next_dt + timedelta(days=30)

        if next_dt <= window_end:
            upcoming.append({
                "id": rem.id,
                "user_id": rem.user_id,
                "product_id": rem.product_id,
                "title": rem.title,
                "description": rem.description,
                "reminder_type": rem.reminder_type,
                "reminder_time": rem.reminder_time.isoformat() if rem.reminder_time else None,
                "frequency": rem.frequency,
                "is_active": rem.is_active,
                "next_occurrence": next_dt.isoformat(),
            })

    # sort by next_occurrence
    upcoming.sort(key=lambda x: x["next_occurrence"])
    return upcoming
