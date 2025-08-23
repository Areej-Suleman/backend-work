from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import (
    LoginRequest, LoginResponse,
    RegisterRequest, RegisterResponse,
    ForgotPasswordRequest, ForgotPasswordResponse,
    ResetPasswordRequest, ResetPasswordResponse
)
from app.core.db import get_db
from app import crud, schemas
router = APIRouter()

@router.post("/")
def chat(message: schemas.ChatMessage):
    response = crud.chat.generate_response(message.text)
    return {"response": response}