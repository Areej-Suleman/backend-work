from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.db import get_db
from app import schemas
from app.crud.users import authenticate_user, create_access_token, get_user_by_email, create_user, update_user
from app.core.permissions import get_current_authenticated_user, get_user_role
from fastapi.security import OAuth2PasswordRequestForm
from app.core.email import email_service, generate_verification_token, get_verification_expires
from app.models.user import User as UserModel


router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2 Password flow login compatible with Swagger's Authorize dialog.

    Accepts application/x-www-form-urlencoded with fields 'username' and 'password'.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Please verify your email before logging in.")
    token = create_access_token(user.id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": get_user_role(user),
            "is_admin": get_user_role(user) == "admin"
        }
    }

@router.post("/register")
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        # If user exists but is not verified, resend verification email
        if not existing_user.is_verified:
            verification_token = generate_verification_token()
            verification_expires = get_verification_expires()
            update_user(db, existing_user.id, {"verification_token": verification_token, "verification_expires": verification_expires})
            email_service.send_verification_email(existing_user.email, existing_user.full_name, verification_token)
            return {"message": "Verification email resent. Please check your inbox."}
        else:
            raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    user = create_user(db, user_data)

    # Generate and set verification token
    verification_token = generate_verification_token()
    verification_expires = get_verification_expires()
    update_user(db, user.id, {"verification_token": verification_token, "verification_expires": verification_expires})

    # Send verification email
    email_service.send_verification_email(user.email, user.full_name, verification_token)

    return {"message": "Registration successful. Please check your email to verify your account."}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    """Verify user's email address."""
    user = db.query(UserModel).filter(UserModel.verification_token == token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid verification token.")

    if user.verification_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Verification token has expired.")

    if user.is_verified:
        return {"message": "Email already verified."}

    update_user(db, user.id, {"is_verified": True, "verification_token": None, "verification_expires": None})

    # Send success email
    email_service.send_verification_success_email(user.email, user.full_name)

    return {"message": "Email verified successfully. You can now log in."}


@router.post("/logout")
def logout():
    return {"message": "Successfully logged out"}

@router.get("/me")
def get_current_user_info(
    current_user: UserModel = Depends(get_current_authenticated_user)
):
    """Get current user information including role"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "skin_type": current_user.skin_type,
        "skin_color": current_user.skin_color,
        "role": get_user_role(current_user),
        "is_admin": get_user_role(current_user) == "admin",
        "created_at": current_user.created_at
    }

@router.post("/forgot-password")
def forgot_password(email: schemas.EmailRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # TODO: Send password reset email
    return {"message": "Password reset email sent"}