"""Pydantic schemas for API requests and responses"""

from app.schemas.coach import CoachCreate, CoachListResponse, CoachResponse, CoachUpdate
from app.schemas.job import JobCreate, JobListResponse, JobResponse, JobUpdate
from app.schemas.match import (
    CoachMatchesResponse,
    CoachMatchResult,
    FitScoreBreakdown,
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
