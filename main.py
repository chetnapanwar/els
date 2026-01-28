import sys
from pathlib import Path

# Add the current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from app.routes.user_routes import router as user_router


# Create FastAPI app instance
app = FastAPI(
    title="User Management API",
    description="API for creating and managing users",
    version="1.0.0"
)


# Include routers
app.include_router(user_router)


# Root endpoint
@app.get("/", tags=["root"])
async def read_root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to User Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
