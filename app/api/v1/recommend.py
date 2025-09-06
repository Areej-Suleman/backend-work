from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.db import get_db
from app import crud, schemas
from app.services.recommender import RecommendationService

router = APIRouter()

@router.post("/{user_id}")
def recommend_products(user_id: int, db: Session = Depends(get_db)):
    recommendations = crud.recommend.generate_for_user(db, user_id)
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found")
    # Persist the generated recommendations for history
    rec_set = crud.recommendations.save_generated(db, user_id, recommendations, title="products")
    return {"recommendations": recommendations, "saved_id": rec_set.id}


@router.post("/{user_id}/skincare")
def recommend_skincare(
    user_id: int,
    preferences: schemas.ProfilePreferences,   # contains preferred_brands, budget_range
    db: Session = Depends(get_db)
):
    recommender = RecommendationService()
    recommendations = recommender.recommend_skincare_routine(
        user_id=user_id,
        preferred_brands=preferences.preferred_brands,
        budget_range=preferences.budget_range,
        db=db
    )
    # Persist set
    rec_set = crud.recommendations.save_generated(db, user_id, recommendations, title="skincare")
    return {"skincare_recommendations": recommendations, "saved_id": rec_set.id}


@router.post("/{user_id}/makeup")
def recommend_makeup(
    user_id: int,
    preferences: schemas.MakeupPreferences,
    db: Session = Depends(get_db)
):
    recommender = RecommendationService()
    recommendations = recommender.recommend_makeup_products(
        user_id=user_id,
        skin_tone=preferences.skin_tone,
        occasion=preferences.occasion,
        style=preferences.style,
        budget_range=preferences.budget_range,
        db=db
    )
    rec_set = crud.recommendations.save_generated(db, user_id, recommendations, title="makeup")
    return {"makeup_recommendations": recommendations, "saved_id": rec_set.id}


@router.post("/{user_id}/personalized")
def get_personalized_recommendations(
    user_id: int,
    filters: Optional[schemas.RecommendationFilters] = None,
    db: Session = Depends(get_db)
):
    recommender = RecommendationService()
    filt = filters.dict() if hasattr(filters, "dict") else (filters or None)
    recommendations = recommender.get_personalized_recommendations(
        user_id=user_id,
        filters=filt,
        db=db
    )
    rec_set = crud.recommendations.save_generated(db, user_id, recommendations, title="personalized", filters=filt)
    return {"personalized_recommendations": recommendations, "saved_id": rec_set.id}


@router.get("/{user_id}/trending")
def get_trending_recommendations(user_id: int, db: Session = Depends(get_db)):
    recommender = RecommendationService()
    trending = recommender.get_trending_products_for_user(user_id, db)
    return {"trending_recommendations": trending}
