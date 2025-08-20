# app/api/auth/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.db.database import get_db
from app.models.user import User
from app.core.config import settings
from app.api.users import users as crud_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Utility function to decode JWT token and get current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud_user.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

# Ensure user is active
def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Restrict access to admin/superuser
def get_current_active_superuser(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
# Ensure user is part of a specific tenant
def get_current_tenant_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.tenant:
        raise HTTPException(status_code=403, detail="User does not belong to any tenant")
    return current_user
# Ensure user is part of a specific tenant and has admin rights
def get_current_tenant_admin_user(current_user: User = Depends(get_current_tenant_user),):
    role_names = {role.name for role in current_user.roles}

    if "admin" not in role_names:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required for tenant operations",
        )    
    return current_user

# Ensure user is part of a specific tenant and has admin rights or is a superuser
def get_current_tenant_admin_user_or_superuser(
    current_user: User = Depends(get_current_user),
):
    # Allow global superuser
    if current_user.is_superuser:
        return current_user

    # Allow tenant admin (has "admin" role)
    role_names = {role.name for role in current_user.roles}
    if "admin" in role_names:
        return current_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin access required (tenant admin or superuser)."
    )