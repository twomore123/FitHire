"""SQLAlchemy models

Import all models here so Alembic can detect them for migrations.
"""

from app.db.session import Base  # noqa: F401
from app.models.brand import Brand, Region, Location  # noqa: F401
from app.models.user import User, UserScope  # noqa: F401
from app.models.coach import Coach  # noqa: F401
from app.models.job import Job  # noqa: F401
from app.models.audit import AuditLog, MatchEvent  # noqa: F401

# Export all models
__all__ = [
    "Base",
    "Brand",
    "Region",
    "Location",
    "User",
    "UserScope",
    "Coach",
    "Job",
    "AuditLog",
    "MatchEvent",
]