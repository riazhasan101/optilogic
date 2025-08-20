# app/api/auth/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional

# -----------------------------
# Auth Related Schemas
# -----------------------------

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# -----------------------------
# User Related Schemas
# -----------------------------

class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    full_name: Optional[str] = None
    password: str
    tenant_id: int
    role_id: int


class UserOut(UserBase):
    id: int
    full_name: Optional[str] = None
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str
