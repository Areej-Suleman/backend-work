from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app import schemas
from app.crud.users import authenticate_user, create_access_token  # 👈 direct imports

router = APIRouter()

@router.post("/login")
def login(user_credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}