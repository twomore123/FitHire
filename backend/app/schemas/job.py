"""Pydantic schemas for Job endpoints"""

from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator


class JobCreate(BaseModel):
    """Schema for creating a new job listing"""
    location_id: int = Field(..., description="Location ID for this job")
    title: str = Field(..., min_length=1, max_length=200, description="Job title")
    description: str = Field(..., description="Full job description")

    # Role requirements
    role_type: str = Field(
        ...,
        description="Role type: Group Fitness Instructor, Personal Trainer, Yoga Instructor, Pilates Instructor"
    )
    required_certifications: List[str] = Field(
        default_factory=list,
        description="Required certifications (must have all)"
    )
    preferred_certifications: List[str] = Field(
        default_factory=list,
        description="Preferred certifications (bonus points)"
    )
    min_experience: int = Field(0, ge=0, description="Minimum years of experience")

    # Schedule requirements
    required_availability: List[str] = Field(
        default_factory=list,
        description="Required time slots (e.g., 'Mon AM', 'Wed PM')"
    )

    # Location
    city: str = Field(..., description="City where job is located")
    state: str = Field(..., max_length=2, description="2-letter state code")

    # Cultural fit
    culture_tags: List[str] = Field(
        default_factory=list,
        description="Desired cultural fit tags"
    )

    # Compensation (optional for Phase 1)
    compensation_type: Optional[str] = Field(None, description="hourly, salary, per_class")
    compensation_min: Optional[Decimal] = Field(None, description="Minimum compensation")
    compensation_max: Optional[Decimal] = Field(None, description="Maximum compensation")

    # FitScore configuration
    weighting_preset: str = Field(
        "balanced",
        description="Weighting preset: balanced, experience_heavy, culture_heavy, availability_focused"
    )
    fitscore_threshold: Decimal = Field(
        Decimal("0.60"),
        ge=Decimal("0.40"),
        le=Decimal("0.80"),
        description="Minimum FitScore threshold (0.40-0.80)"
    )

    @field_validator('role_type')
    @classmethod
    def validate_role_type(cls, v: str) -> str:
        allowed_roles = [
            "Group Fitness Instructor",
            "Personal Trainer",
            "Yoga Instructor",
            "Pilates Instructor"
        ]
        if v not in allowed_roles:
            raise ValueError(f"role_type must be one of: {', '.join(allowed_roles)}")
        return v

    @field_validator('weighting_preset')
    @classmethod
    def validate_preset(cls, v: str) -> str:
        allowed_presets = ["balanced", "experience_heavy", "culture_heavy", "availability_focused"]
        if v not in allowed_presets:
            raise ValueError(f"weighting_preset must be one of: {', '.join(allowed_presets)}")
        return v


class JobUpdate(BaseModel):
    """Schema for updating an existing job listing"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None

    role_type: Optional[str] = None
    required_certifications: Optional[List[str]] = None
    preferred_certifications: Optional[List[str]] = None
    min_experience: Optional[int] = Field(None, ge=0)

    required_availability: Optional[List[str]] = None

    city: Optional[str] = None
    state: Optional[str] = Field(None, max_length=2)

    culture_tags: Optional[List[str]] = None

    compensation_type: Optional[str] = None
    compensation_min: Optional[Decimal] = None
    compensation_max: Optional[Decimal] = None

    weighting_preset: Optional[str] = None
    fitscore_threshold: Optional[Decimal] = Field(None, ge=Decimal("0.40"), le=Decimal("0.80"))

    status: Optional[str] = None

    @field_validator('role_type')
    @classmethod
    def validate_role_type(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed_roles = [
            "Group Fitness Instructor",
            "Personal Trainer",
            "Yoga Instructor",
            "Pilates Instructor"
        ]
        if v not in allowed_roles:
            raise ValueError(f"role_type must be one of: {', '.join(allowed_roles)}")
        return v

    @field_validator('weighting_preset')
    @classmethod
    def validate_preset(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed_presets = ["balanced", "experience_heavy", "culture_heavy", "availability_focused"]
        if v not in allowed_presets:
            raise ValueError(f"weighting_preset must be one of: {', '.join(allowed_presets)}")
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed_statuses = ["draft", "open", "filled", "closed"]
        if v not in allowed_statuses:
            raise ValueError(f"status must be one of: {', '.join(allowed_statuses)}")
        return v


class JobResponse(BaseModel):
    """Schema for job listing responses"""
    id: int
    location_id: int
    brand_id: int

    title: str
    description: str

    role_type: str
    required_certifications: List[str]
    preferred_certifications: List[str]
    min_experience: int

    required_availability: List[str]

    city: str
    state: str

    culture_tags: List[str]

    compensation_type: Optional[str]
    compensation_min: Optional[float]
    compensation_max: Optional[float]

    weighting_preset: str
    fitscore_threshold: float

    status: str

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    """Schema for paginated job list"""
    jobs: List[JobResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
