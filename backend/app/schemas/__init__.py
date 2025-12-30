"""Pydantic schemas for API requests and responses"""

from app.schemas.coach import CoachCreate, CoachUpdate, CoachResponse, CoachListResponse
from app.schemas.job import JobCreate, JobUpdate, JobResponse, JobListResponse
from app.schemas.match import (
    FitScoreBreakdown,
    CoachMatchResult,
    CoachMatchesResponse,
    JobCandidateResult,
    JobCandidatesResponse,
)

__all__ = [
    "CoachCreate",
    "CoachUpdate",
    "CoachResponse",
    "CoachListResponse",
    "JobCreate",
    "JobUpdate",
    "JobResponse",
    "JobListResponse",
    "FitScoreBreakdown",
    "CoachMatchResult",
    "CoachMatchesResponse",
    "JobCandidateResult",
    "JobCandidatesResponse",
]
