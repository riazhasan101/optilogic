from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from app.api.tenant import router as tenant_router
from app.api.users import router as user_router
from app.api.sales import router as sales_router
from app.api.auth import auth

# Import the SIMPLE database module
from app.db.database_simple import Base, engine, SessionLocal

# Define lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
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

# Log startup message
logger.info("Starting Optilogic API application")

# Include API routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tenant_router.router, tags=["tenant"])
app.include_router(user_router.router, tags=["user"])
app.include_router(sales_router.router, tags=["sales"])

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