from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base
import logging
import os

# Import all model files so SQLAlchemy sees them
from app.models import user, role, page, pages_roles, tenant, users_roles

# DEBUG: Log environment variables
logger = logging.getLogger(__name__)
logger.info("Environment variables: %s", dict(os.environ))

# Get DATABASE_URL from environment (Railway provides this)
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Production - use Railway's DATABASE_URL
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")
    logger.info("Using DATABASE_URL from environment: %s", DATABASE_URL)
else:
    # Development - use settings (but this should NOT happen on Railway)
    DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI
    logger.warning("Using settings-based URL (this should not happen in production): %s", DATABASE_URL)

# SQLAlchemy engine with appropriate configuration
if DATABASE_URL and DATABASE_URL.startswith('sqlite'):
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False},
        echo=True
    )
else:
    # PostgreSQL configuration
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
        echo=True
    )

# SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully.")
        logger.info("Using database: %s", DATABASE_URL)
    except Exception as e:
        logger.error(f"Error while creating tables: {e}")
        raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()