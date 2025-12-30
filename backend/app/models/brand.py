"""Brand, Region, and Location models for organizational hierarchy"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class Brand(Base):
    """
    Top-level organization (e.g., Equinox, SoulCycle)
    """

    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    regions = relationship("Region", back_populates="brand", cascade="all, delete-orphan")
    users = relationship("User", back_populates="brand")
    coaches = relationship("Coach", back_populates="brand")
    jobs = relationship("Job", back_populates="brand")

    def __repr__(self):
        return f"<Brand(id={self.id}, name='{self.name}')>"


class Region(Base):
    """
    Regional subdivision of a brand (e.g., Northeast, West Coast)
    """

    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    brand = relationship("Brand", back_populates="regions")
    locations = relationship("Location", back_populates="region", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Region(id={self.id}, name='{self.name}', brand_id={self.brand_id})>"


class Location(Base):
    """
    Physical studio/gym location within a region
    """

    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    region = relationship("Region", back_populates="locations")
    brand = relationship("Brand")
    jobs = relationship("Job", back_populates="location")

    def __repr__(self):
        return f"<Location(id={self.id}, name='{self.name}', city='{self.city}')>"
