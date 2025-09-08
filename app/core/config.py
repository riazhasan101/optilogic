<<<<<<< HEAD
from pydantic_settings import BaseSettings  # Updated import
from typing import Optional

class Settings(BaseSettings):
    # Database configuration
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"  # Default to localhost if not specified
    DB_PORT: int = 5432        # Default to PostgreSQL default port
    DB_NAME: str

    # Optional: Add more configuration parameters as needed
    SECRET_KEY: str=""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Default token expiry time
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
=======
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # These are ONLY for development
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "optilogic_dev"
    
    # This will be None in development, set by Railway in production
    DATABASE_URL: Optional[str] = os.environ.get('DATABASE_URL')
    
    # JWT settings
    SECRET_KEY: str = "change-this-in-production-make-a-strong-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Use DATABASE_URL if available, otherwise build from components
        if self.DATABASE_URL:
            return self.DATABASE_URL.replace("postgres://", "postgresql://")
>>>>>>> feebf2c2da559a058a6924018213ef3598c83061
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
<<<<<<< HEAD
    class Config:
        env_file = ".env"  # Load environment variables from a .env file

# Instantiate the settings object
settings = Settings()
=======

    class Config:
        env_file = ".env"

settings = Settings()
>>>>>>> feebf2c2da559a058a6924018213ef3598c83061
