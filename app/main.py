from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import engine, Base
from auth import optional_auth, verify_api_key

# Create the database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI Project Template",
    version="1.0.0",
    docs_url="/docs" if settings.enable_swagger else None,
    redoc_url="/redoc" if settings.enable_swagger else None,
    debug=settings.debug
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Health check endpoint (no auth required)
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is up and running."}


# Protected endpoint example
@app.get("/protected")
async def protected_endpoint(auth: bool = Depends(verify_api_key)):
    return {"message": "This is a protected endpoint", "authenticated": True}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "FastAPI Project Template",
        "docs": "/docs" if settings.enable_swagger else "disabled",
        "health": "/health"
        }