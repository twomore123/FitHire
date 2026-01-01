"""FitHire FastAPI Application Entry Point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.config import settings

# Create FastAPI application
app = FastAPI(
    title="FitHire API",
    description="Fitness professional matching platform with deterministic FitScore algorithm",
    version="0.1.0",
    docs_url="/docs" if settings.is_development else None,  # Disable docs in production
    redoc_url="/redoc" if settings.is_development else None,
)

# Custom CORS middleware to handle Vercel deployment URLs
class CustomCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin")

        # Check if origin is allowed
        allowed = False
        if origin:
            # Allow localhost
            if origin.startswith("http://localhost") or origin.startswith("http://127.0.0.1"):
                allowed = True
            # Allow any Vercel deployment
            elif ".vercel.app" in origin:
                allowed = True
            # Check against configured origins
            elif origin in settings.cors_origins_list:
                allowed = True

        # Handle preflight requests
        if request.method == "OPTIONS":
            if allowed and origin:
                return JSONResponse(
                    content={},
                    headers={
                        "Access-Control-Allow-Origin": origin,
                        "Access-Control-Allow-Methods": "*",
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Credentials": "true",
                    },
                )

        response = await call_next(request)

        # Add CORS headers to response
        if allowed and origin:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "*"

        return response

# Add custom CORS middleware
app.add_middleware(CustomCORSMiddleware)


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
from app.api.v1.routes.coaches import router as coaches_router
from app.api.v1.routes.jobs import router as jobs_router

app.include_router(coaches_router, prefix="/api/v1")
app.include_router(jobs_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )
