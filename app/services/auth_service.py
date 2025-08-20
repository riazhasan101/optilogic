from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from app.core.config import settings
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import verify_password, create_access_token
from app.models.user import User

# OAuth2 scheme


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
class auth:    

    def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
        user = db.query(User).filter(User.username == form_data.username).first()
        
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id, "tenant_id": user.tenant_id},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

# User models
# class User(BaseModel):
#     username: str
#     full_name: str | None = None
#     email: str
#     disabled: bool = False

# class UserInDB(User):
#     hashed_password: str
# class auth:
    
    # JWT settings
    # SECRET_KEY = settings.SECRET_KEY
    # ALGORITHM = settings.ALGORITHM
    # ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    # Dummy user for testing
    # fake_user_db = {
    #     "admin": {
    #         "username": "admin",
    #         "full_name": "Admin User",
    #         "email": "admin@example.com",
    #         "hashed_password": "password123",  # Replace with real hashed pw
    #         "disabled": False
    #     }
    # }

    # Create token
    # def create_access_token(data: dict, expires_delta: timedelta | None = None):
    #     to_encode = data.copy()
    #     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    #     to_encode.update({"exp": expire})
    #     return jwt.encode(to_encode, auth.SECRET_KEY, algorithm=auth.ALGORITHM)

    # # Decode and validate token
    # def verify_token(token: str):
    #     credentials_exception = HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Could not validate credentials",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    #     try:
    #         payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
    #         username = payload.get("sub")
    #         if username is None:
    #             raise credentials_exception
    #         return username
    #     except JWTError:
    #         raise credentials_exception

    # Get user from dummy DB
    # def get_user(username: str):
    #     user = auth.fake_user_db.get(username)
    #     if user:
    #         return UserInDB(**user)

    # # Authenticate user
    # def authenticate_user(username: str, password: str):
    #     user = auth.get_user(username)
    #     if not user or password != user.hashed_password:
    #         return None
    #     return user

    # Public method to generate token
    # async def login_for_access_token(username: str, password: str):
    #     user = auth.authenticate_user(username, password)
    #     if not user:
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail="Incorrect username or password",
    #             headers={"WWW-Authenticate": "Bearer"},
    #         )
    #     access_token = auth.create_access_token(data={"sub": user.username})
    #     return {"access_token": access_token, "token_type": "bearer"}



    # # Dependency to get current user
    # def get_current_user(token: str = Depends(oauth2_scheme)):
    #     username = auth.verify_token(token)
    #     user = auth.get_user(username)
    #     if not user:
    #         raise HTTPException(status_code=404, detail="User not found")
    #     return user

    # # Dependency to check active user
    # def get_current_active_user(current_user: User = Depends(get_current_user)):
    #     if current_user.disabled:
    #         raise HTTPException(status_code=400, detail="Inactive user")
    #     return current_user