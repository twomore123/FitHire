"""Coach model for fitness professional profiles"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.session import Base


class Coach(Base):
    """
    Fitness professional profile with certifications, experience, and preferences
    """

    __tablename__ = "coaches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False, index=True)

    # Basic Info
    bio = Column(Text, nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)

    # Experience
    years_experience = Column(Integer, nullable=False)
    certifications = Column(
        JSONB, nullable=False
    )  # [{"name": "NASM-CPT", "verified": true, "expiration": "2025-12-31"}]
    specialties = Column(JSONB, nullable=True)  # ["HIIT", "Cycling", "Strength Training"]

    # Availability (array of time slots)
    available_times = Column(
        JSONB, nullable=False
    )  # ["Mon AM", "Wed PM", "Fri AM", "Sat AM"]

    # Culture/Style Tags (admin-assigned)
    lifestyle_tags = Column(JSONB, nullable=True)  # ["wellness", "community", "high-energy"]
    movement_tags = Column(JSONB, nullable=True)  # ["technical-precision", "dynamic-flow"]
    instruction_tags = Column(JSONB, nullable=True)  # ["motivational", "educational"]

    # Media
    profile_image_url = Column(String(500), nullable=True)
    verified_video_url = Column(String(500), nullable=True)
    social_links = Column(JSONB, nullable=True)  # {"instagram": "...", "youtube": "..."}

    # Metadata
    profile_completeness = Column(Numeric(3, 2), nullable=True)  # 0.00 to 1.00
    verified_at = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="coach")
    brand = relationship("Brand", back_populates="coaches")

    def __repr__(self):
        return f"<Coach(id={self.id}, user_id={self.user_id}, city='{self.city}')>"
