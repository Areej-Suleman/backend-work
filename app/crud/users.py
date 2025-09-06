from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt
from datetime import datetime, timedelta

from fastapi.security import HTTPBearer
security = HTTPBearer()
from app.core.security import verify_password, create_token, hash_password
from app.core.config import settings
from app.models.user import User
from app.models.profile import Profile
from typing import Any
import json

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    # 'hashed_password' field is the canonical password store
    stored_hash = user.hashed_password
    if not stored_hash or not verify_password(password, stored_hash):
        return None
    return user

def create_access_token(user_id: int) -> str:
    return create_token({"sub": str(user_id)})

def get_current_user(db: Session, token: Any) -> User:
    """Resolve current user from a Bearer token.

    Accepts either an HTTPAuthorizationCredentials object or a raw token string
    (as provided by OAuth2PasswordBearer).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Normalize token
    token_value = getattr(token, "credentials", token)
    try:
        payload = jwt.decode(token_value, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        user_id = int(sub)
    except Exception:
        raise credentials_exception
    user = db.query(User).get(user_id)
    if user is None:
        raise credentials_exception
    return user

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data) -> User:
    # Accept Pydantic model or dict
    data = user_data.dict() if hasattr(user_data, "dict") else dict(user_data)
    raw_password = data.pop("password", None)
    # Prevent privilege escalation from public endpoints
    data.pop("is_admin", None)
    if raw_password:
        data["hashed_password"] = hash_password(raw_password)
    user = User(**data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _parse_text_list(value):
    """Best-effort parser for Text fields that may store lists.
    Accepts JSON strings like '["a","b"]' or comma-separated text like 'a,b'.
    Returns a list of strings. Empty/None -> [].
    """
    if not value:
        return []
    if isinstance(value, list):
        return value
    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return [str(x) for x in parsed]
    except Exception:
        pass
    # Fallback: comma-separated
    return [s.strip() for s in str(value).split(',') if s.strip()]


def get_user_preferences(db: Session, user_id: int):
    """Return the user's saved preferences from their Profile.

    This function is called by the users API: GET /api/v1/users/{user_id}/preferences
    """
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {
        "preferred_brands": _parse_text_list(profile.preferred_brands),
        "budget_range": profile.budget_range,
        "skin_sensitivity": profile.skin_sensitivity,
        "skin_concerns": _parse_text_list(profile.skin_concerns),
        "allergies": _parse_text_list(profile.allergies),
    }

def delete_user(db: Session, user_id: int) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt
from datetime import datetime, timedelta

from fastapi.security import HTTPBearer
security = HTTPBearer()
from app.core.security import verify_password, create_token, hash_password
from app.core.config import settings
from app.models.user import User
from app.models.profile import Profile
from typing import Any
import json

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    # 'hashed_password' field is the canonical password store
    stored_hash = user.hashed_password
    if not stored_hash or not verify_password(password, stored_hash):
        return None
    return user

def create_access_token(user_id: int) -> str:
    return create_token({"sub": str(user_id)})

def get_current_user(db: Session, token: Any) -> User:
    """Resolve current user from a Bearer token.

    Accepts either an HTTPAuthorizationCredentials object or a raw token string
    (as provided by OAuth2PasswordBearer).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Normalize token
    token_value = getattr(token, "credentials", token)
    try:
        payload = jwt.decode(token_value, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        user_id = int(sub)
    except Exception:
        raise credentials_exception
    user = db.query(User).get(user_id)
    if user is None:
        raise credentials_exception
    return user

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data) -> User:
    # Accept Pydantic model or dict
    data = user_data.dict() if hasattr(user_data, "dict") else dict(user_data)
    raw_password = data.pop("password", None)
    # Prevent privilege escalation from public endpoints
    data.pop("is_admin", None)
    if raw_password:
        data["hashed_password"] = hash_password(raw_password)
    user = User(**data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _parse_text_list(value):
    """Best-effort parser for Text fields that may store lists.
    Accepts JSON strings like '["a","b"]' or comma-separated text like 'a,b'.
    Returns a list of strings. Empty/None -> [].
    """
    if not value:
        return []
    if isinstance(value, list):
        return value
    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return [str(x) for x in parsed]
    except Exception:
        pass
    # Fallback: comma-separated
    return [s.strip() for s in str(value).split(',') if s.strip()]


def get_user_preferences(db: Session, user_id: int):
    """Return the user's saved preferences from their Profile.

    This function is called by the users API: GET /api/v1/users/{user_id}/preferences
    """
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {
        "preferred_brands": _parse_text_list(profile.preferred_brands),
        "budget_range": profile.budget_range,
        "skin_sensitivity": profile.skin_sensitivity,
        "skin_concerns": _parse_text_list(profile.skin_concerns),
        "allergies": _parse_text_list(profile.allergies),
    }

def delete_user(db: Session, user_id: int) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()
def update_user(db: Session, user_id: int, user_data) -> Optional[User]:
    """Update a user.

    Accepts either a dict or a Pydantic model (UserUpdate). Only updates fields
    that are actually provided (exclude_unset=True). If a "password" is
    provided, it will be hashed into "hashed_password".
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    # Normalize input to a dict with only provided fields
    if hasattr(user_data, "model_dump"):  # Pydantic v2
        data = user_data.model_dump(exclude_unset=True)
    elif hasattr(user_data, "dict"):  # Pydantic v1 compatibility
        data = user_data.dict(exclude_unset=True)
    else:
        data = dict(user_data or {})

    # Handle password update securely
    raw_password = data.pop("password", None)
    if raw_password:
        data["hashed_password"] = hash_password(raw_password)

    for key, value in data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def get_all(db: Session):
    return db.query(User).all()

def count_all(db: Session) -> int:
    return db.query(User).count()

def get_recent_signups(db: Session, days: int = 7):
    start_date = datetime.utcnow() - timedelta(days=days)
    return db.query(User).filter(User.created_at >= start_date).all()

