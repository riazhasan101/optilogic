from pydantic_settings import BaseSettings  # Updated import
from typing import Optional

# class Settings(BaseSettings):
#     # Database configuration
#     DB_USER: str
#     DB_PASSWORD: str
#     DB_HOST: str = "localhost"  # Default to localhost if not specified
#     DB_PORT: int = 5432        # Default to PostgreSQL default port
#     DB_NAME: str

#     # Optional: Add more configuration parameters as needed
#     SECRET_KEY: str=""
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Default token expiry time

# Database configuration with defaults
class Settings(BaseSettings):
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "optilogic"
    
    SECRET_KEY: str = "change-this-in-production-make-it-very-secret"
    ALGORCHEMY: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    class Config:
        env_file = ".env"  # Load environment variables from a .env file

# Instantiate the settings object
settings = Settings()
