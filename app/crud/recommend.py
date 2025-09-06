from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.services.recommender import RecommendationService


def generate_for_user(db: Session, user_id: int) -> List[Dict[str, Any]]:
    """Return a basic set of recommendations for a user.
    Currently proxies to a simple "trending products for user" method.
    """
    service = RecommendationService()
    # Fallback: use trending as a baseline
    return service.get_trending_products_for_user(user_id, db)
