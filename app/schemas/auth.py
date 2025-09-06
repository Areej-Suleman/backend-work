# app/schemas/auth.py

from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: EmailStr
    full_name: str
    skin_type: str
    skin_color: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    skin_type: str
    skin_color: str

class RegisterResponse(BaseModel):
    message: str

class EmailRequest(BaseModel):
    email: EmailStr


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ForgotPasswordResponse(BaseModel):
    message: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class ResetPasswordResponse(BaseModel):
    message: str
