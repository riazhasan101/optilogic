# app/api/users/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str
    tenant_id: int

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserOut(UserBase):
    id: int
    tenant_id: int

    class Config:
        from_attributes = True