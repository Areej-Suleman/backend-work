from sqlalchemy.orm import Session

from app.models import ChatbotLog

def generate_response(text: str) -> str:
    t = (text or "").lower().strip()

    if "hello" in t or "hi" in t:
        return "Hey there! How can I help you with your skincare today?"
    elif "recommend" in t or "suggest" in t:
        return "Sure! Can you tell me your skin type and what you're looking for?"
    elif "dry skin" in t:
        return "For dry skin, I recommend using a hydrating cleanser and a moisturizer with hyaluronic acid."
    elif "oily skin" in t:
        return "For oily skin, try a gentle foaming cleanser and a lightweight, oil-free moisturizer."
    elif "thank you" in t or "thanks" in t:
        return "You're welcome! Let me know if you need anything else."
    elif "bye" in t or "goodbye" in t:
        return "Take care! Hope your skin glows brighter than ever."
    else:
        return "I'm still learning! Could you rephrase that or tell me more about your skin concerns?"

def log_conversation(
    db: Session,
    user_id: int,
    message: str,
    response: str,
    session_id: str | None = None,
    intent: str | None = None,
    confidence_score: str | None = None,
):
    log = ChatbotLog(
        user_id=user_id,
        message=message,
        response=response,
        session_id=session_id,
        intent=intent,
        confidence_score=confidence_score,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_user_chat_history(db: Session, user_id: int):
    return (
        db.query(ChatbotLog)
        .filter(ChatbotLog.user_id == user_id)
        .order_by(ChatbotLog.created_at.desc())
        .all()
    )
