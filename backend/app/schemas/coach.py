"""Pydantic schemas for Coach endpoints"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class CertificationItem(BaseModel):
    """Individual certification"""

    name: str = Field(..., description="Certification name (e.g., 'NASM-CPT', 'ACE')")
    issued_date: Optional[str] = Field(None, description="ISO date when issued")
    expiry_date: Optional[str] = Field(None, description="ISO date when expires")
    credential_id: Optional[str] = Field(None, description="Credential ID or number")


class CoachCreate(BaseModel):
    """Schema for creating a new coach profile"""

    location_id: int = Field(..., description="Location ID this coach belongs to")
    city: str = Field(..., description="City where coach is based")
    state: str = Field(..., max_length=2, description="2-letter state code")

    # Professional details
    certifications: List[CertificationItem] = Field(
        default_factory=list, description="List of certifications"
    )
    years_experience: int = Field(0, ge=0, description="Years of professional experience")

    # Availability
    available_times: List[str] = Field(
        default_factory=list, description="Available time slots (e.g., 'Mon AM', 'Wed PM')"
    )

    # Cultural fit tags
    lifestyle_tags: List[str] = Field(default_factory=list, description="Lifestyle approach tags")
    movement_tags: List[str] = Field(default_factory=list, description="Movement style tags")
    instruction_tags: List[str] = Field(default_factory=list, description="Instruction style tags")

    # Media
    profile_photo_url: Optional[HttpUrl] = None
    verified_video_url: Optional[HttpUrl] = None

    # Bio
    bio: Optional[str] = Field(None, max_length=2000, description="Professional bio")


class CoachUpdate(BaseModel):
    """Schema for updating an existing coach profile"""

    city: Optional[str] = None
    state: Optional[str] = Field(None, max_length=2)

    certifications: Optional[List[CertificationItem]] = None
    years_experience: Optional[int] = Field(None, ge=0)

    available_times: Optional[List[str]] = None

    lifestyle_tags: Optional[List[str]] = None
    movement_tags: Optional[List[str]] = None
    instruction_tags: Optional[List[str]] = None

    profile_photo_url: Optional[HttpUrl] = None
    verified_video_url: Optional[HttpUrl] = None

    bio: Optional[str] = Field(None, max_length=2000)


class CoachResponse(BaseModel):
    """Schema for coach profile responses"""

    id: int
    user_id: int
    brand_id: int

    # Basic Info
    city: str
    state: str
    bio: Optional[str] = None

    # Experience
    years_experience: int
    certifications: List[dict]
    specialties: Optional[List[str]] = None

    # Availability
    available_times: List[str]

    # Cultural fit tags
    lifestyle_tags: Optional[List[str]] = None
    movement_tags: Optional[List[str]] = None
    instruction_tags: Optional[List[str]] = None

    # Media
    profile_image_url: Optional[str] = None
    verified_video_url: Optional[str] = None
    social_links: Optional[dict] = None

    # Metadata
    profile_completeness: Optional[float] = None
    verified_at: Optional[datetime] = None
    last_updated: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class CoachListResponse(BaseModel):
    """Schema for paginated coach list"""

    coaches: List[CoachResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
