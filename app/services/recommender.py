from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.product import Product
from app.models.brand import Brand

class RecommendationService:
    def __init__(self):
        self.recommendation_weights = {
            "skin_type": 0.4,
            "skin_tone": 0.3,
            "concerns": 0.2,
            "preferences": 0.1
        }

    def _parse_budget(self, budget_range: Optional[str]) -> Optional[float]:
        if not budget_range:
            return None
        s = str(budget_range).strip()
        # formats: "25000" or "1000-5000"
        if "-" in s:
            try:
                _min, _max = s.split("-", 1)
                return float(_max.strip())
            except Exception:
                pass
        try:
            return float(s)
        except Exception:
            return None

    def _filter_and_shape(self, products: List[Product], preferred_brands: Optional[List[str]] = None, max_price: Optional[float] = None) -> List[Dict[str, Any]]:
        pb = [b.lower() for b in (preferred_brands or [])]
        out: List[Dict[str, Any]] = []
        for p in products:
            if max_price is not None and p.price is not None and p.price > max_price:
                continue
            if pb:
                brand_name = p.brand.name.lower() if p.brand and p.brand.name else ""
                if not any(b in brand_name for b in pb):
                    continue
            out.append({
                "id": p.id,
                "name": p.name,
                "brand": p.brand.name if p.brand else None,
                "category": p.category,
                "price": p.price,
                "score": 0.6,  # simple static score for now
                "reasons": ["Matches your preferences"] if pb or max_price else ["Popular choice"],
                "image_url": p.images[0].image_url if getattr(p, "images", None) else None,
            })
        # fallback: if nothing matched, return first few products
        if not out:
            for p in products[:10]:
                out.append({
                    "id": p.id,
                    "name": p.name,
                    "brand": p.brand.name if p.brand else None,
                    "category": p.category,
                    "price": p.price,
                    "score": 0.5,
                    "reasons": ["Popular choice"],
                    "image_url": p.images[0].image_url if getattr(p, "images", None) else None,
                })
        return out

    def get_trending_products_for_user(self, user_id: int, db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        """Simple synchronous helper used by some endpoints.
        Returns a basic list of products as "trending" for the user.
        """
        products = db.query(Product).limit(limit).all()
        results: List[Dict[str, Any]] = []
        for product in products:
            results.append({
                "id": product.id,
                "name": product.name,
                "brand": product.brand.name if product.brand else None,
                "category": product.category,
                "price": product.price,
                "score": 0.5,
                "reasons": ["Popular choice"],
                "image_url": product.images[0].image_url if getattr(product, "images", None) else None,
            })
        return results

    def recommend_skincare_routine(self, *, user_id: int, preferred_brands: Optional[List[str]] = None, budget_range: Optional[str] = None, db: Session) -> List[Dict[str, Any]]:
        max_price = self._parse_budget(budget_range)
        products = db.query(Product).filter(Product.category == "skincare").all()
        return self._filter_and_shape(products, preferred_brands, max_price)

    def recommend_makeup_products(self, *, user_id: int, skin_tone: Optional[str] = None, occasion: Optional[str] = None, style: Optional[str] = None, budget_range: Optional[str] = None, db: Session) -> List[Dict[str, Any]]:
        max_price = self._parse_budget(budget_range)
        products = db.query(Product).filter(Product.category == "makeup").all()
        # For now ignore skin_tone/occasion/style; could be used to score later
        return self._filter_and_shape(products, None, max_price)

    def get_personalized_recommendations(self, *, user_id: int, filters: Optional[Dict[str, Any]], db: Session) -> List[Dict[str, Any]]:
        category = (filters or {}).get("category") if isinstance(filters, dict) else None
        min_price = (filters or {}).get("min_price") if isinstance(filters, dict) else None
        max_price = (filters or {}).get("max_price") if isinstance(filters, dict) else None
        brands = (filters or {}).get("brands") if isinstance(filters, dict) else None

        q = db.query(Product)
        if category:
            q = q.filter(Product.category == category)
        products = q.all()
        shaped = self._filter_and_shape(products, brands, max_price)
        if min_price is not None:
            shaped = [p for p in shaped if p.get("price") is None or p.get("price") >= float(min_price)]
        return shaped

    async def get_product_recommendations(
        self, 
        db: Session, 
        user_id: int, 
        category: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get personalized product recommendations for user"""
        
        # Get user profile
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.profile:
            return await self._get_popular_products(db, category, limit)
        
        # Get user preferences from profile
        user_profile = user.profile
        
        # Get all products
        query = db.query(Product)
        if category:
            query = query.filter(Product.category == category)
        
        products = query.all()
        
        # Score products based on user profile
        scored_products = []
        for product in products:
            score = self._calculate_product_score(product, user_profile)
            scored_products.append({
                "product": product,
                "score": score,
                "reasons": self._get_recommendation_reasons(product, user_profile)
            })
        
        # Sort by score and return top recommendations
        scored_products.sort(key=lambda x: x["score"], reverse=True)
        
        return [
            {
                "id": item["product"].id,
                "name": item["product"].name,
                "brand": item["product"].brand.name if item["product"].brand else None,
                "category": item["product"].category,
                "price": item["product"].price,
                "score": item["score"],
                "reasons": item["reasons"],
                "image_url": item["product"].images[0].image_url if item["product"].images else None
            }
            for item in scored_products[:limit]
        ]

    def _calculate_product_score(self, product: Product, user_profile) -> float:
        """Calculate recommendation score for a product"""
        score = 0.0
        
        # Skin type matching
        if hasattr(user_profile, 'skin_type') and user_profile.skin_type:
            if product.suitable_skin_types and user_profile.skin_type in product.suitable_skin_types:
                score += self.recommendation_weights["skin_type"]
        
        # Skin tone matching
        if hasattr(user_profile, 'skin_tone') and user_profile.skin_tone:
            # This would need more sophisticated matching logic
            score += self.recommendation_weights["skin_tone"] * 0.5
        
        # Concerns matching
        if hasattr(user_profile, 'skin_concerns') and user_profile.skin_concerns:
            if product.targets_concerns:
                concern_overlap = set(user_profile.skin_concerns) & set(product.targets_concerns)
                if concern_overlap:
                    score += self.recommendation_weights["concerns"] * (len(concern_overlap) / len(user_profile.skin_concerns))
        
        # Add base popularity score
        score += 0.1
        
        return min(score, 1.0)  # Cap at 1.0

    def _get_recommendation_reasons(self, product: Product, user_profile) -> List[str]:
        """Get reasons why this product is recommended"""
        reasons = []
        
        if hasattr(user_profile, 'skin_type') and user_profile.skin_type:
            if product.suitable_skin_types and user_profile.skin_type in product.suitable_skin_types:
                reasons.append(f"Perfect for {user_profile.skin_type} skin")
        
        if hasattr(user_profile, 'skin_concerns') and user_profile.skin_concerns:
            if product.targets_concerns:
                concern_overlap = set(user_profile.skin_concerns) & set(product.targets_concerns)
                for concern in concern_overlap:
                    reasons.append(f"Targets {concern}")
        
        if not reasons:
            reasons.append("Popular choice")
        
        return reasons

    async def _get_popular_products(self, db: Session, category: Optional[str], limit: int) -> List[Dict[str, Any]]:
        """Get popular products when no user profile available"""
        query = db.query(Product)
        if category:
            query = query.filter(Product.category == category)
        
        products = query.limit(limit).all()
        
        return [
            {
                "id": product.id,
                "name": product.name,
                "brand": product.brand.name if product.brand else None,
                "category": product.category,
                "price": product.price,
                "score": 0.5,
                "reasons": ["Popular choice"],
                "image_url": product.images[0].image_url if product.images else None
            }
            for product in products
        ]

    async def get_shade_recommendations(
        self, 
        db: Session, 
        user_id: int, 
        product_category: str = "foundation"
    ) -> List[Dict[str, Any]]:
        """Get shade recommendations based on user's skin tone"""
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.profile:
            return []
        
        # This would use the shade matching service
        # For now, return placeholder data
        return [
            {
                "shade_name": "Medium Beige",
                "hex_code": "#D4A574",
                "match_confidence": 0.95,
                "undertone": "warm"
            }
        ]

# Global recommendation service instance
recommendation_service = RecommendationService()
