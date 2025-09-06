from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.db import get_db
from app import crud, schemas
from app.services.recommender import RecommendationService

router = APIRouter()

@router.get("/{user_id}")
def get_saved_recommendations(user_id: int, db: Session = Depends(get_db), since: Optional[str] = None, until: Optional[str] = None):
    from datetime import datetime
    parse = lambda s: datetime.fromisoformat(s) if s else None
    saved = crud.recommendations.get_for_user(db, user_id, since=parse(since), until=parse(until))
    if not saved:
        raise HTTPException(status_code=404, detail="No saved recommendations")
    return saved

@router.post("/{user_id}")
def save_recommendation(user_id: int, rec: schemas.RecommendationCreate, db: Session = Depends(get_db)):
    saved = crud.recommendations.save(db, user_id, rec)
    return {"saved_id": saved.id}

@router.get("/{user_id}/by-category/{category}")
def get_recommendations_by_category(
    user_id: int, 
    category: str, 
    db: Session = Depends(get_db)
):
    recommendations = crud.recommendations.get_by_category(db, user_id, category)
    return {"recommendations": recommendations, "category": category}

@router.delete("/{user_id}/{recommendation_id}")
def delete_recommendation(
    user_id: int, 
    recommendation_id: int, 
    db: Session = Depends(get_db)
):
    crud.recommendations.delete(db, user_id, recommendation_id)
    return {"message": "Recommendation deleted successfully"}

@router.put("/{user_id}/{recommendation_id}/rating")
def rate_recommendation(
    user_id: int,
    recommendation_id: int,
    rating: schemas.RecommendationRating,
    db: Session = Depends(get_db)
):
    return crud.recommendations.update_rating(db, user_id, recommendation_id, rating.rating)
