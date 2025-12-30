"""Job model for job listings"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.session import Base


class Job(Base):
    """
    Job listing posted by hiring managers
    """

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False, index=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Job Details
    title = Column(String(255), nullable=False)
    role_type = Column(
        String(100), nullable=False, index=True
    )  # 'group_fitness_instructor', 'personal_trainer', 'yoga_instructor', 'pilates_instructor'
    description = Column(Text, nullable=True)

    # Requirements
    required_certifications = Column(JSONB, nullable=False)  # ["NASM-CPT", "ACE"]
    preferred_certifications = Column(JSONB, nullable=True)  # ["RYT-200"]
    min_experience = Column(Integer, nullable=False)  # years
    required_availability = Column(JSONB, nullable=False)  # ["Mon AM", "Wed PM", "Fri AM"]

    # Location
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)

    # Culture
    culture_tags = Column(JSONB, nullable=True)  # ["community", "high-energy", "wellness"]

    # Scoring
    weighting_preset = Column(
        String(50), nullable=False, default="balanced"
    )  # 'balanced', 'experience_heavy', 'culture_heavy', 'availability_focused'
    fitscore_threshold = Column(Numeric(3, 2), default=0.60)  # 0.00 to 1.00

    # Compensation (optional, not used in scoring v1)
    compensation_min = Column(Integer, nullable=True)
    compensation_max = Column(Integer, nullable=True)

    # Status
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    brand = relationship("Brand", back_populates="jobs")
    location = relationship("Location", back_populates="jobs")
    created_by_user = relationship("User")

    def __repr__(self):
        return f"<Job(id={self.id}, title='{self.title}', role_type='{self.role_type}')>"
