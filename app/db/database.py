from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base
import logging
import os

# Import all model files so SQLAlchemy sees them
from app.models import user, role, page, pages_roles, tenant, users_roles

# Determine database URL - use DATABASE_URL if provided (Railway/Production), otherwise build from components
if os.environ.get('DATABASE_URL'):
    # Production - use the provided connection string
    DATABASE_URL = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://")
else:
    # Development - build from individual components
    DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# SQLAlchemy engine with appropriate configuration
if DATABASE_URL.startswith('sqlite'):
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False},
        echo=True  # Set to False in production
    )
else:
    # PostgreSQL configuration
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,           # Adjust based on your needs
        max_overflow=10,       # Adjust based on your needs
        pool_timeout=30,       # 30 seconds
        pool_recycle=1800,     # Recycle connections after 30 minutes
        echo=True             # Set to False in production
    )

# SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Logging
logger = logging.getLogger(__name__)

def create_db_and_tables():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully.")
        
        # Log database type for debugging
        if DATABASE_URL.startswith('sqlite'):
            logger.info("Using SQLite database")
        else:
            logger.info("Using PostgreSQL database")
            
    except Exception as e:
        logger.error(f"Error while creating tables: {e}")
        raise

def get_db():
    """
    Dependency to get database session.
    Use this in your FastAPI route dependencies.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Optional: Function to check database connection
def check_database_connection():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False