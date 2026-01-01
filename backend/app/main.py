"""FitHire FastAPI Application Entry Point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings

# Create FastAPI application
app = FastAPI(
    title="FitHire API",
    description="Fitness professional matching platform with deterministic FitScore algorithm",
    version="0.1.0",
    docs_url="/docs" if settings.is_development else None,  # Disable docs in production
    redoc_url="/redoc" if settings.is_development else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Service status and environment information
    """
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "fithire-backend",
            "version": "0.1.0",
            "environment": settings.environment,
        }
    )


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint.

    Returns:
        dict: API welcome message
    """
    return {
        "message": "Welcome to FitHire API",
        "version": "0.1.0",
        "docs": "/docs" if settings.is_development else "Documentation disabled in production",
        "routes_loaded": True,
    }


# API v1 routes
from app.api.v1.routes import coaches, jobs

app.include_router(coaches.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )
