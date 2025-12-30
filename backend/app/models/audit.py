"""Audit logging and match event tracking models"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.session import Base


class AuditLog(Base):
    """
    Tracks all important system events and changes for compliance and debugging
    """

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Event Details
    event_type = Column(
        String(100), nullable=False, index=True
    )  # 'profile_updated', 'job_created', 'match_viewed', 'score_recalculated'
    entity_type = Column(String(50), nullable=True)  # 'coach', 'job', 'match'
    entity_id = Column(Integer, nullable=True)

    # Changes (JSONB for flexibility)
    changes = Column(
        JSONB, nullable=True
    )  # {"old_score": 0.75, "new_score": 0.82, "reason": "certification_added"}

    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    ip_address = Column(String(50), nullable=True)

    # Relationships
    brand = relationship("Brand")
    user = relationship("User")

    def __repr__(self):
        return f"<AuditLog(id={self.id}, event_type='{self.event_type}', timestamp='{self.timestamp}')>"


class MatchEvent(Base):
    """
    Tracks match-related events for future ML training

    Examples: viewed, applied, interviewed, hired, rejected
    """

    __tablename__ = "match_events"

    id = Column(Integer, primary_key=True, index=True)
    coach_id = Column(Integer, ForeignKey("coaches.id"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False, index=True)

    # Event
    event = Column(
        String(50), nullable=False, index=True
    )  # 'viewed', 'applied', 'interviewed', 'hired', 'rejected'
    fitscore_at_event = Column(Numeric(5, 3), nullable=True)  # Score when event occurred

    # Actor
    triggered_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # Who caused this event

    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    coach = relationship("Coach")
    job = relationship("Job")
    brand = relationship("Brand")
    user = relationship("User")

    def __repr__(self):
        return f"<MatchEvent(id={self.id}, event='{self.event}', coach_id={self.coach_id}, job_id={self.job_id})>"
