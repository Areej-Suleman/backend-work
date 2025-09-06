from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app import crud, schemas
from app.services.chatbot import ChatbotService

router = APIRouter()

@router.post("/")
def chat(message: schemas.ChatMessage, db: Session = Depends(get_db)):
    chatbot_service = ChatbotService()
    response = chatbot_service.generate_response(message.text, message.user_id)
    
    # Log the conversation
    crud.chat.log_conversation(db, message.user_id, message.text, response)
    
    return {"response": response, "user_id": message.user_id}

@router.post("/skincare-advice")
def get_skincare_advice(
    request: schemas.SkincareAdviceRequest, 
    db: Session = Depends(get_db)
):
    chatbot_service = ChatbotService()
    advice = chatbot_service.get_skincare_advice(
        skin_type=request.skin_type,
        concerns=request.concerns,
        age=request.age,
        budget=request.budget
    )
    
    return {"advice": advice, "user_id": request.user_id}

@router.get("/{user_id}/history")
def get_chat_history(user_id: int, db: Session = Depends(get_db)):
    history = crud.chat.get_user_chat_history(db, user_id)
    return {"chat_history": history}
