from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.users.schemas import UserOut, UserCreate, UserUpdate
from app.api.users import users as user_crud
from app.db.database import get_db
from app.api.auth.dependencies import get_current_active_user, get_current_active_superuser,get_current_tenant_admin_user_or_superuser
from app.models.user import User
from app.core.security import ensure_same_tenant

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserOut])
def read_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_tenant_admin_user_or_superuser),
):
    if current_user.is_superuser:
        return user_crud.get_users(db)

    return db.query(User).filter(User.tenant_id == current_user.tenant_id).all()
  

@router.get("/{user_id}", response_model=UserOut)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_user = user_crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/", response_model=UserOut)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_tenant_admin_user_or_superuser),
):
    if not current_user.is_superuser and user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot create user in another tenant.")

    existing = user_crud.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    return user_crud.create_user(db, user)

@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    updates: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_tenant_admin_user_or_superuser),
):
    db_user = user_crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    ensure_same_tenant(current_user, db_user)
    return user_crud.update_user(db, db_user, updates)

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_tenant_admin_user_or_superuser),
):
    db_user = user_crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    ensure_same_tenant(current_user, db_user)
    user_crud.delete_user(db, user_id)
    return {"detail": "User deleted successfully"}


# Returns logged-in user info
@router.get("/me", response_model=UserOut)
def get_logged_in_user(
    current_user: User = Depends(get_current_active_user),
):
    return current_user