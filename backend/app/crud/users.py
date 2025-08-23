from sqlalchemy.orm import Session
from app.models import User
from app.core.security import verify_password, create_token

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(user_id: int):
    return create_token({"sub": str(user_id)})
