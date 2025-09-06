import google.generativeai
from app.core.config import settings
from typing import List, Optional

class ChatbotService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            google.generativeai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = google.generativeai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None # Or raise an error, or log a warning

    def generate_response(self, text: str, user_id: int) -> str:
        t = (text or "").lower().strip()
        
        # Rule-based responses
        if any(g in t for g in ["hello", "hi", "hey"]):
            return "Hey there! How can I help you with your skincare today?"
        if "recommend" in t or "suggest" in t:
            return "Sure! Tell me me your skin type and concerns, and I’ll suggest products."
        if "dry skin" in t:
            return "For dry skin, use a hydrating cleanser and a moisturizer with hyaluronic acid."
        if "oily skin" in t:
            return "For oily skin, try a gentle foaming cleanser and an oil-free moisturizer."
        if "thank" in t:
            return "You're welcome! Anything else I can do?"
        if "bye" in t or "goodbye" in t:
            return "Take care! Hope your skin glows brighter than ever."
        
        # Fallback to Gemini API if no rule-based response matches
        if self.model:
            try:
                response = self.model.generate_content(text)
                return response.text
            except Exception as e:
                print(f"Error calling Gemini API: {e}")
                return "I'm having trouble connecting to my knowledge base right now. Please try again later."
        
        return "I'm still learning! Could you rephrase that or tell me more about your skin concerns?"

    def get_skincare_advice(
        self,
        skin_type: Optional[str] = None,
        concerns: Optional[List[str]] = None,
        age: Optional[int] = None,
        budget: Optional[float] = None,
    ) -> List[str]:
        concerns = concerns or []
        tips: List[str] = []
        if skin_type == "dry":
            tips += [
                "Use a gentle, hydrating cleanser.",
                "Layer hyaluronic acid serum under a ceramide moisturizer.",
                "Avoid hot water and harsh exfoliants.",
            ]
        elif skin_type == "oily":
            tips += [
                "Use a foaming cleanser.",
                "Look for niacinamide and salicylic acid.",
                "Choose non-comedogenic, oil-free moisturizers.",
            ]
        elif skin_type == "combination":
            tips += [
                "Use a balanced cleanser.",
                "Spot treat oily T-zone with BHA.",
                "Lightweight moisturizer overall; richer on dry patches.",
            ]
        if "acne" in concerns:
            tips.append("Introduce benzoyl peroxide or adapalene (start slow).")
        if "wrinkles" in concerns:
            tips.append("Use retinol at night; daily SPF 30+.")
        if "dark_spots" in concerns:
            tips.append("Try vitamin C in the morning and azelaic acid at night.")
        return tips
