# from sqlalchemy import create_engine, MetaData
# from sqlalchemy.orm import sessionmaker
# from app.core.config import settings
# from app.db.base import Base  # This Base is already used by your models
# import logging

# # Import all model files so SQLAlchemy sees them
# from app.models import user, role, page, pages_roles, tenant,users_roles  # Add all your model files here

# # Database URL
# DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# # SQLAlchemy engine
# engine = create_engine(DATABASE_URL, echo=True)

# # SessionLocal
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Logging
# logger = logging.getLogger(__name__)

# def create_db_and_tables():
#     try:
#         Base.metadata.create_all(bind=engine)
#         logger.info("Tables created successfully.")
#     except Exception as e:
#         logger.error(f"Error while creating tables: {e}")
#         raise

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.core.config import settings
from app.db.base import Base  # This Base is already used by your models
import logging
import time

# Import all model files so SQLAlchemy sees them
from app.models import user, role, page, pages_roles, tenant, users_roles

<<<<<<< HEAD
# Logging
logger = logging.getLogger(__name__)

# Database URL
DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# Retry settings
MAX_RETRIES = 5
WAIT_SECONDS = 5

# SQLAlchemy engine with retry
engine = None
for attempt in range(1, MAX_RETRIES + 1):
    try:
        engine = create_engine(DATABASE_URL, echo=True)
        Base.metadata.create_all(bind=engine)
        logger.info("Database connected and tables created successfully.")
        break
    except OperationalError as e:
        logger.warning(f"Database connection failed (attempt {attempt}/{MAX_RETRIES}): {e}")
        if attempt == MAX_RETRIES:
            logger.error("Max retries reached. Exiting.")
            raise
        time.sleep(WAIT_SECONDS)
=======
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
>>>>>>> feebf2c2da559a058a6924018213ef3598c83061

# SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
<<<<<<< HEAD
    """Keep your function for backward compatibility."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully.")
=======
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully.")
        logger.info("Using database: %s", DATABASE_URL)
>>>>>>> feebf2c2da559a058a6924018213ef3598c83061
    except Exception as e:
        logger.error(f"Error while creating tables: {e}")
        raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
<<<<<<< HEAD
        db.close()

=======
        db.close()
>>>>>>> feebf2c2da559a058a6924018213ef3598c83061
