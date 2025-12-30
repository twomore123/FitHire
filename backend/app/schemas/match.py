"""Pydantic schemas for Match/FitScore endpoints"""

from typing import List
from pydantic import BaseModel, Field

from app.schemas.coach import CoachResponse
from app.schemas.job import JobResponse


class FitScoreBreakdown(BaseModel):
    """Detailed breakdown of FitScore components"""
    fitscore: float = Field(..., description="Overall FitScore (0.0 to 1.0)")
    cert_score: float = Field(..., description="Certifications match score")
    experience_score: float = Field(..., description="Experience match score")
    availability_score: float = Field(..., description="Availability match score")
    location_score: float = Field(..., description="Location match score")
    culture_score: float = Field(..., description="Cultural fit score")
    engagement_score: float = Field(..., description="Engagement signals score")


class CoachMatchResult(BaseModel):
    """A job match for a coach"""
    job: JobResponse
    fitscore: float
    score_breakdown: FitScoreBreakdown
    rank: int = Field(..., description="Rank in the match list (1-20)")


class CoachMatchesResponse(BaseModel):
    """Response with top job matches for a coach"""
    coach_id: int
    matches: List[CoachMatchResult]
    total_matches: int = Field(..., description="Total number of matches above threshold")
    threshold: float = Field(..., description="FitScore threshold used for filtering")


class JobCandidateResult(BaseModel):
    """A coach candidate for a job"""
    coach: CoachResponse
    fitscore: float
    score_breakdown: FitScoreBreakdown
    rank: int = Field(..., description="Rank in the candidate list (1-20)")


class JobCandidatesResponse(BaseModel):
    """Response with top coach candidates for a job"""
    job_id: int
    candidates: List[JobCandidateResult]
    total_candidates: int = Field(..., description="Total number of candidates above threshold")
    threshold: float = Field(..., description="FitScore threshold used for filtering")
