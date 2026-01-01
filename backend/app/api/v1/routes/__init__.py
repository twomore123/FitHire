"""API v1 routes"""

# Import routers for external use
from .coaches import router as coaches_router
from .jobs import router as jobs_router

__all__ = ["coaches_router", "jobs_router"]
