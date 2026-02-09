from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routes import tasks
from .db import create_db_and_tables
from .schemas import HealthCheck
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the database tables
# Commenting out for now to avoid import issues during testing
# create_db_and_tables()

# Create FastAPI app instance
app = FastAPI(
    title="Todo API",
    description="REST API for the Full-Stack Todo Application",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose authorization header to client applications
    expose_headers=["Access-Control-Allow-Origin", "Authorization"]
)

# Include the task routes
app.include_router(tasks.router)


@app.on_event("startup")
async def startup_event():
    """
    Event handler for application startup.
    Initializes the database and performs any necessary startup tasks.
    """
    print("Starting up the Todo API application...")
    create_db_and_tables()
    print("Database tables created successfully.")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Event handler for application shutdown.
    Performs any necessary cleanup tasks.
    """
    print("Shutting down the Todo API application...")


@app.get("/")
async def root():
    """
    Root endpoint for the API.
    Returns a welcome message and basic API information.
    """
    return {
        "message": "Welcome to the Todo API",
        "version": "1.0.0",
        "documentation": "/docs",
        "description": "REST API for the Full-Stack Todo Application with JWT authentication"
    }


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """
    Health check endpoint.
    Returns the health status of the API.
    """
    return HealthCheck(
        status="healthy",
        timestamp=datetime.utcnow()
    )


@app.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint.
    Returns the readiness status of the API.
    """
    # Add any additional checks here (e.g., database connectivity)
    return {"status": "ready"}


# Additional utility endpoints can be added here

if __name__ == "__main__":
    import uvicorn
    # Get port from environment variable or default to 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)