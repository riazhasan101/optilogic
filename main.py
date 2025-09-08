<<<<<<< HEAD
# main.py (clean version)
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.db.database import create_db_and_tables
=======
from contextlib import asynccontextmanager
from fastapi import FastAPI
>>>>>>> feebf2c2da559a058a6924018213ef3598c83061
import logging
from app.api.tenant import router as tenant_router
from app.api.users import router as user_router
from app.api.sales import router as sales_router
from app.api.auth import auth

<<<<<<< HEAD
=======
# Import the SIMPLE database module
from app.db.database_simple import Base, engine, SessionLocal

>>>>>>> feebf2c2da559a058a6924018213ef3598c83061
# Define lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
<<<<<<< HEAD
        create_db_and_tables()
        logger.info("Database connected and tables created.")
        yield
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        raise
=======
        # Create tables using the simple database connection
        Base.metadata.create_all(bind=engine)
        logger.info("Database connected and tables created successfully.")
        
        # Test connection
        with SessionLocal() as db:
            db.execute("SELECT 1")
            logger.info("Database connection test passed")
            
        yield
        
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        # Don't raise the error completely, just log it
        # This allows the app to start even if database fails
        yield
>>>>>>> feebf2c2da559a058a6924018213ef3598c83061

# Create FastAPI instance
app = FastAPI(
    title="Optilogic API",
    description="An API for managing tenants, users, authentication, and sales forecasting.",
    version="1.0.0",
    lifespan=lifespan
)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

<<<<<<< HEAD
=======
# Log startup message
logger.info("Starting Optilogic API application")

>>>>>>> feebf2c2da559a058a6924018213ef3598c83061
# Include API routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tenant_router.router, tags=["tenant"])
app.include_router(user_router.router, tags=["user"])
app.include_router(sales_router.router, tags=["sales"])

<<<<<<< HEAD
# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to Optilogic API2!"}


# to run with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
=======
# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Optilogic API is running"}

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to Optilogic API!"}

# Run with uvicorn
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
>>>>>>> feebf2c2da559a058a6924018213ef3598c83061
