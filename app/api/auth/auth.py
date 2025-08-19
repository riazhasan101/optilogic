from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import auth as auth_service
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter()

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    return  auth_service.login_for_access_token(form_data, db)

# @router.get("/me")
# async def get_current_user(user: dict = Depends(auth_service.get_current_active_user)):
#     return user