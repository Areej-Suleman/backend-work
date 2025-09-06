from typing import Optional, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException
import json

from app.models.profile import Profile
from app.models.user import User


def _dump_list(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, list):
        return json.dumps(value)
    return str(value)


def get_by_user_id(db: Session, user_id: int) -> Optional[Profile]:
    return db.query(Profile).filter(Profile.user_id == user_id).first()


def create(db: Session, profile_data) -> Profile:
    # Accept Pydantic model or dict
    data = profile_data.model_dump() if hasattr(profile_data, "model_dump") else (
        profile_data.dict() if hasattr(profile_data, "dict") else dict(profile_data)
    )

    user_id = data.get("user_id")

    # Pull out skin fields meant for User table
    skin_type = data.pop("skin_type", None)
    skin_tone = data.pop("skin_tone", None)

    # Normalize list-like fields to JSON strings
    if "skin_concerns" in data:
        data["skin_concerns"] = _dump_list(data.get("skin_concerns"))
    if "allergies" in data:
        data["allergies"] = _dump_list(data.get("allergies"))
    if "preferred_brands" in data:
        data["preferred_brands"] = _dump_list(data.get("preferred_brands"))

    # If a profile already exists for this user, update it instead of inserting a duplicate
    existing = get_by_user_id(db, user_id)
    if existing:
        for key, value in data.items():
            setattr(existing, key, value)
        profile = existing
    else:
        profile = Profile(**data)
        db.add(profile)

    # Update corresponding User.skin_type and User.skin_color
    user = db.query(User).filter(User.id == profile.user_id).first()
    if user is not None:
        if skin_type is not None:
            user.skin_type = skin_type
        if skin_tone is not None:
            user.skin_color = skin_tone
        db.add(user)

    db.commit()
    db.refresh(profile)
    return profile


def update_user(db: Session, user_id: int, profile_update) -> Optional[Profile]:
    profile = get_by_user_id(db, user_id)
    if not profile:
        return None

    if hasattr(profile_update, "model_dump"):
        data = profile_update.model_dump(exclude_unset=True)
    elif hasattr(profile_update, "dict"):
        data = profile_update.dict(exclude_unset=True)
    else:
        data = dict(profile_update or {})

    # Extract skin fields for User model
    skin_type = data.pop("skin_type", None)
    skin_tone = data.pop("skin_tone", None)

    # Normalize list-like fields
    if "skin_concerns" in data:
        data["skin_concerns"] = _dump_list(data.get("skin_concerns"))
    if "allergies" in data:
        data["allergies"] = _dump_list(data.get("allergies"))
    if "preferred_brands" in data:
        data["preferred_brands"] = _dump_list(data.get("preferred_brands"))

    for key, value in data.items():
        setattr(profile, key, value)

    # Update related user
    user = db.query(User).filter(User.id == user_id).first()
    if user is not None:
        if skin_type is not None:
            user.skin_type = skin_type
        if skin_tone is not None:
            user.skin_color = skin_tone
        db.add(user)

    db.commit()
    db.refresh(profile)
    return profile


def update_preferences(db: Session, user_id: int, preferences) -> Optional[Profile]:
    profile = get_by_user_id(db, user_id)
    if not profile:
        return None
    # Extract payload
    if hasattr(preferences, "model_dump"):
        data = preferences.model_dump(exclude_unset=True)
    elif hasattr(preferences, "dict"):
        data = preferences.dict(exclude_unset=True)
    else:
        data = dict(preferences or {})

    # Only update the declared preference fields
    if "preferred_brands" in data:
        profile.preferred_brands = _dump_list(data.get("preferred_brands"))
    if "budget_range" in data:
        profile.budget_range = data.get("budget_range")

    db.commit()
    db.refresh(profile)
    return profile


def delete_by_user_id(db: Session, user_id: int) -> bool:
    profile = get_by_user_id(db, user_id)
    if not profile:
        return False
    db.delete(profile)
    db.commit()
    return True
