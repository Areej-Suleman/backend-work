from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app import crud, schemas

router = APIRouter()

@router.put("/{user_id}", response_model=schemas.Profile)
def update_profile(user_id: int, profile: schemas.ProfileUpdate, db: Session = Depends(get_db)):
    updated = crud.profile.update_user(db, user_id, profile)
    if not updated:
        raise HTTPException(status_code=404, detail="Profile not found")
    return updated

@router.get("/{user_id}", response_model=schemas.Profile)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = crud.profile.get_by_user_id(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/", response_model=schemas.Profile)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    return crud.profile.create(db, profile)

@router.delete("/{user_id}")
def delete_profile(user_id: int, db: Session = Depends(get_db)):
    success = crud.profile.delete_by_user_id(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"detail": "Profile deleted successfully"}

@router.get("/{user_id}/skin-analysis")
def get_skin_analysis(user_id: int, db: Session = Depends(get_db)):
    profile = crud.profile.get_by_user_id(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    # skin fields live on User table
    return {
        "skin_type": getattr(profile.user, "skin_type", None),
        "skin_tone": getattr(profile.user, "skin_color", None),
        "skin_concerns": profile.skin_concerns,
        "allergies": profile.allergies,
    }

@router.put("/{user_id}/preferences", response_model=schemas.Profile)
def update_preferences(user_id: int, preferences: schemas.ProfilePreferences, db: Session = Depends(get_db)):
    updated = crud.profile.update_preferences(db, user_id, preferences)
    if not updated:
        raise HTTPException(status_code=404, detail="Profile not found")
    return updated
