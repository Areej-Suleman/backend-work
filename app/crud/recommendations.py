from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from app.models.recommendation import Recommendation, RecommendationItem
from app.models.product import Product


def save(db: Session, user_id: int, rec_payload) -> Recommendation:
    """Save a recommendation set provided by the client.
    rec_payload may be a Pydantic model with product_ids and reason fields.
    """
    data = rec_payload.dict() if hasattr(rec_payload, "dict") else dict(rec_payload)
    reason = data.get("reason")
    product_ids: List[int] = data.get("product_ids") or []

    rec = Recommendation(user_id=user_id, reason=reason, created_at=datetime.utcnow())
    db.add(rec)
    db.flush()  # get rec.id

    rank = 1
    for pid in product_ids:
        item = RecommendationItem(
            recommendation_id=rec.id,
            product_id=pid,
            score=None,
            reason=None,
            rank=rank,
        )
        db.add(item)
        rank += 1

    db.commit()
    db.refresh(rec)
    return rec


def save_generated(db: Session, user_id: int, generated_items: List[Dict[str, Any]], title: Optional[str] = None, filters: Optional[Dict[str, Any]] = None) -> Recommendation:
    """Persist items returned by a recommender run."""
    rec = Recommendation(
        user_id=user_id,
        title=title or "auto",
        reason="auto-generated",
        filters=json.dumps(filters) if filters else None,
        created_at=datetime.utcnow(),
    )
    db.add(rec)
    db.flush()

    for idx, it in enumerate(generated_items, start=1):
        product_id = it.get("id") or it.get("product_id")
        reasons = it.get("reasons")
        item = RecommendationItem(
            recommendation_id=rec.id,
            product_id=product_id,
            score=it.get("score"),
            reason=", ".join(reasons) if isinstance(reasons, list) else (reasons or None),
            rank=idx,
        )
        db.add(item)

    db.commit()
    db.refresh(rec)
    return rec


def get_for_user(db: Session, user_id: int, since: Optional[datetime] = None, until: Optional[datetime] = None) -> List[Recommendation]:
    q = db.query(Recommendation).filter(Recommendation.user_id == user_id)
    if since:
        q = q.filter(Recommendation.created_at >= since)
    if until:
        q = q.filter(Recommendation.created_at <= until)
    return q.order_by(Recommendation.created_at.desc()).all()


def get_by_category(db: Session, user_id: int, category: str) -> List[Recommendation]:
    # Return recommendation sets that contain at least one item with a product in the given category
    return (
        db.query(Recommendation)
        .join(Recommendation.items)
        .join(RecommendationItem.product)
        .filter(Recommendation.user_id == user_id, Product.category == category)
        .order_by(Recommendation.created_at.desc())
        .all()
    )


def delete(db: Session, user_id: int, recommendation_id: int) -> None:
    rec = db.query(Recommendation).filter(Recommendation.id == recommendation_id, Recommendation.user_id == user_id).first()
    if not rec:
        return
    db.delete(rec)
    db.commit()


def update_rating(db: Session, user_id: int, recommendation_id: int, rating: int) -> Recommendation:
    rec = db.query(Recommendation).filter(Recommendation.id == recommendation_id, Recommendation.user_id == user_id).first()
    if not rec:
        return None
    rec.rating = rating
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec
