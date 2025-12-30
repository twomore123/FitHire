"""Job CRUD and candidate matching endpoints"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime

from app.db.session import get_db
from app.models.job import Job
from app.models.coach import Coach
from app.models.brand import Location
from app.schemas.job import JobCreate, JobUpdate, JobResponse, JobListResponse
from app.schemas.match import JobCandidatesResponse, JobCandidateResult, FitScoreBreakdown
from app.utils.auth import get_current_user
from app.core.fitscore.engine import FitScoreEngine

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new job listing

    Requires authentication. Users can only create jobs in their authorized locations.
    """
    # Verify location exists and user has access
    location = db.query(Location).filter(Location.id == job_data.location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location {job_data.location_id} not found"
        )

    # Create job
    new_job = Job(
        brand_id=location.brand_id,
        location_id=job_data.location_id,
        title=job_data.title,
        description=job_data.description,
        role_type=job_data.role_type,
        required_certifications=job_data.required_certifications,
        preferred_certifications=job_data.preferred_certifications,
        min_experience=job_data.min_experience,
        required_availability=job_data.required_availability,
        city=job_data.city,
        state=job_data.state,
        culture_tags=job_data.culture_tags,
        compensation_type=job_data.compensation_type,
        compensation_min=job_data.compensation_min,
        compensation_max=job_data.compensation_max,
        weighting_preset=job_data.weighting_preset,
        fitscore_threshold=job_data.fitscore_threshold,
        status="draft"  # New jobs start as draft
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get a single job listing by ID

    Requires authentication.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found"
        )

    return job


@router.get("/", response_model=JobListResponse)
async def list_jobs(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    location_id: Optional[int] = Query(None, description="Filter by location"),
    role_type: Optional[str] = Query(None, description="Filter by role type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    List jobs with pagination and filtering

    Requires authentication. Users see jobs in their authorized locations.
    """
    query = db.query(Job)

    # Apply filters
    if location_id:
        query = query.filter(Job.location_id == location_id)
    if role_type:
        query = query.filter(Job.role_type == role_type)
    if status:
        query = query.filter(Job.status == status)

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * page_size
    jobs = query.order_by(Job.created_at.desc()).offset(offset).limit(page_size).all()

    return JobListResponse(
        jobs=jobs,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.patch("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_update: JobUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update a job listing

    Requires authentication. Only updates provided fields (partial update).
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found"
        )

    # Update fields if provided
    update_data = job_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(job, field, value)

    # Update timestamp
    job.updated_at = datetime.now()

    db.commit()
    db.refresh(job)

    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a job listing

    Requires authentication and appropriate permissions.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found"
        )

    db.delete(job)
    db.commit()

    return None


@router.get("/{job_id}/candidates", response_model=JobCandidatesResponse)
async def get_job_candidates(
    job_id: int,
    limit: int = Query(20, ge=1, le=20, description="Maximum number of candidates to return"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get top coach candidates for a job

    Returns coaches ranked by FitScore, filtered by the job's threshold.
    Only returns coaches with status='verified'.
    """
    # Get job
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found"
        )

    # Get all verified coaches in the same city (Phase 1: exact city match only)
    coaches = db.query(Coach).filter(
        and_(
            Coach.status == "verified",
            Coach.city == job.city,
            Coach.state == job.state,
            Coach.role_type == job.role_type  # Must match role type
        )
    ).all()

    # Calculate FitScore for each coach
    engine = FitScoreEngine()
    candidates = []

    # Prepare job data for FitScore engine
    job_data = {
        "required_certifications": job.required_certifications,
        "preferred_certifications": job.preferred_certifications,
        "min_experience": job.min_experience,
        "required_availability": job.required_availability,
        "city": job.city,
        "state": job.state,
        "culture_tags": job.culture_tags,
    }

    threshold = float(job.fitscore_threshold) if job.fitscore_threshold else 0.60

    for coach in coaches:
        coach_data = {
            "certifications": coach.certifications,
            "years_experience": coach.years_experience,
            "available_times": coach.available_times,
            "city": coach.city,
            "state": coach.state,
            "lifestyle_tags": coach.lifestyle_tags,
            "movement_tags": coach.movement_tags,
            "instruction_tags": coach.instruction_tags,
            "profile_completeness": float(coach.profile_completeness) if coach.profile_completeness else 0.0,
            "last_updated": coach.last_updated.isoformat() if coach.last_updated else None,
            "verified_video_url": coach.verified_video_url,
        }

        score = engine.calculate_match(
            coach_data,
            job_data,
            preset=job.weighting_preset
        )

        # Only include if above threshold
        if score.fitscore >= threshold:
            candidates.append({
                "coach": coach,
                "score": score
            })

    # Sort by FitScore descending
    candidates.sort(key=lambda x: x["score"].fitscore, reverse=True)

    # Limit to top N candidates
    candidates = candidates[:limit]

    # Format response
    candidate_results = []
    for rank, candidate in enumerate(candidates, start=1):
        candidate_results.append(JobCandidateResult(
            coach=candidate["coach"],
            fitscore=candidate["score"].fitscore,
            score_breakdown=FitScoreBreakdown(
                fitscore=candidate["score"].fitscore,
                cert_score=candidate["score"].cert_score,
                experience_score=candidate["score"].experience_score,
                availability_score=candidate["score"].availability_score,
                location_score=candidate["score"].location_score,
                culture_score=candidate["score"].culture_score,
                engagement_score=candidate["score"].engagement_score,
            ),
            rank=rank
        ))

    return JobCandidatesResponse(
        job_id=job_id,
        candidates=candidate_results,
        total_candidates=len(candidates),
        threshold=threshold
    )
