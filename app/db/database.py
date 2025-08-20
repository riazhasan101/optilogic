from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base  # This Base is already used by your models
import logging

# Import all model files so SQLAlchemy sees them
from app.models import user, role, page, pages_roles, tenant,users_roles  # Add all your model files here

# Database URL
DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Logging
logger = logging.getLogger(__name__)

def create_db_and_tables():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully.")
    except Exception as e:
        logger.error(f"Error while creating tables: {e}")
        raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
