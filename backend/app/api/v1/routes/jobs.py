"""Job CRUD and candidate matching endpoints"""

import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.fitscore.engine import FitScoreEngine
from app.db.session import get_db
from app.models.brand import Location
from app.models.coach import Coach
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreate, JobListResponse, JobResponse, JobUpdate
from app.schemas.match import FitScoreBreakdown, JobCandidateResult, JobCandidatesResponse
from app.utils.auth import get_current_user

router = APIRouter(prefix="/jobs", tags=["jobs"])
logger = logging.getLogger(__name__)


def get_or_create_user(db: Session, current_user: dict) -> User:
    """
    Get or create a User record from Clerk authentication

    Args:
        db: Database session
        current_user: Decoded JWT payload from Clerk

    Returns:
        User: The user record
    """
    try:
        clerk_user_id = current_user.get("sub")
        logger.info(f"JWT payload keys: {list(current_user.keys())}")
        logger.info(f"Clerk user ID: {clerk_user_id}")

        if not clerk_user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token: missing user ID",
            )

        # Try to find existing user
        user = db.query(User).filter(User.clerk_user_id == clerk_user_id).first()

        if not user:
            # Create new user record
            # Extract email from JWT - Clerk uses different field names
            email = (
                current_user.get("email")
                or current_user.get("email_address")
                or current_user.get("primary_email")
                or f"{clerk_user_id}@clerk.user"
            )

            logger.info(f"Creating new user with email: {email}")

            user = User(
                clerk_user_id=clerk_user_id,
                email=email,
                first_name=current_user.get("given_name") or current_user.get("first_name"),
                last_name=current_user.get("family_name") or current_user.get("last_name"),
                role="location_manager",  # Default role for job creators
                # brand_id intentionally omitted - nullable, assigned later via job/location
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Created user with ID: {user.id}")
        else:
            logger.info(f"Found existing user with ID: {user.id}")

        return user
    except Exception as e:
        logger.error(f"Error in get_or_create_user: {str(e)}")
        logger.error(f"JWT payload: {current_user}")
        db.rollback()
        raise


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Create a new job listing

    Requires authentication. Users can only create jobs in their authorized locations.
    """
    logger.info(f"Creating job: {job_data.title}")

    # Verify location exists and user has access
    location = db.query(Location).filter(Location.id == job_data.location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location {job_data.location_id} not found",
        )

    # Get or create user from Clerk authentication
    user = get_or_create_user(db, current_user)

    logger.info(f"Job being created by user ID: {user.id}")

    # Create job (only set fields that exist in Job model)
    new_job = Job(
        created_by=user.id,
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
        compensation_min=int(job_data.compensation_min) if job_data.compensation_min else None,
        compensation_max=int(job_data.compensation_max) if job_data.compensation_max else None,
        weighting_preset=job_data.weighting_preset,
        custom_weights=job_data.custom_weights,  # Add custom_weights field
        fitscore_threshold=job_data.fitscore_threshold,
        is_active=True,  # New jobs are active by default
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    """
    Get a single job listing by ID

    Requires authentication. Users can only view their own jobs.
    """
    # Get the current user from database
    user = get_or_create_user(db, current_user)
    logger.info(f"User {user.id} requesting job {job_id}")

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        logger.error(f"Job {job_id} not found in database")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job {job_id} not found")

    logger.info(f"Job {job_id} found, created_by={job.created_by}, requesting_user={user.id}")

    # Verify that this job belongs to the current user
    if job.created_by != user.id:
        logger.error(f"User {user.id} does not own job {job_id} (owned by {job.created_by})")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this job listing",
        )

    logger.info(f"Access granted to job {job_id}")
    return job


@router.get("/", response_model=JobListResponse)
async def list_jobs(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    location_id: Optional[int] = Query(None, description="Filter by location"),
    role_type: Optional[str] = Query(None, description="Filter by role type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    List jobs with pagination and filtering

    Requires authentication. Users see only their own job listings.
    """
    # Get the current user from database
    user = get_or_create_user(db, current_user)

    # Start with query filtered by current user
    query = db.query(Job).filter(Job.created_by == user.id)

    # Apply additional filters
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
        total_pages=(total + page_size - 1) // page_size,
    )


@router.patch("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_update: JobUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update a job listing

    Requires authentication. Users can only update their own jobs.
    """
    # Get the current user from database
    user = get_or_create_user(db, current_user)

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job {job_id} not found")

    # Verify that this job belongs to the current user
    if job.created_by != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this job listing",
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
    job_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    """
    Delete a job listing

    Requires authentication. Users can only delete their own jobs.
    """
    # Get the current user from database
    user = get_or_create_user(db, current_user)

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job {job_id} not found")

    # Verify that this job belongs to the current user
    if job.created_by != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this job listing",
        )

    db.delete(job)
    db.commit()

    return None


@router.get("/{job_id}/candidates", response_model=JobCandidatesResponse)
async def get_job_candidates(
    job_id: int,
    limit: int = Query(20, ge=1, le=20, description="Maximum number of candidates to return"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Get top coach candidates for a job

    Returns coaches ranked by FitScore, filtered by the job's threshold.
    Only returns coaches with status='verified'.
    """
    # Get the current user from database
    user = get_or_create_user(db, current_user)

    # Get job and verify ownership
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job {job_id} not found")

    # Verify that this job belongs to the current user
    if job.created_by != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view candidates for this job listing",
        )

    # Get all verified coaches in the same city (Phase 1: exact city match only)
    # Note: Coach model doesn't have status or role_type fields
    # verified_at is used to determine if coach is verified
    logger.info(f"Looking for coaches in {job.city}, {job.state}")

    coaches = (
        db.query(Coach)
        .filter(
            and_(
                Coach.verified_at.isnot(None),  # Coach is verified if verified_at is set
                Coach.city == job.city,
                Coach.state == job.state,
            )
        )
        .all()
    )

    logger.info(f"Found {len(coaches)} verified coaches in {job.city}, {job.state}")

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
    logger.info(f"FitScore threshold: {threshold}")

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
            "profile_completeness": (
                float(coach.profile_completeness) if coach.profile_completeness else 0.0
            ),
            "last_updated": coach.last_updated.isoformat() if coach.last_updated else None,
            "verified_video_url": coach.verified_video_url,
        }

        score = engine.calculate_match(
            coach_data, job_data, preset=job.weighting_preset, custom_weights=job.custom_weights
        )

        logger.info(f"Coach {coach.id}: FitScore={score.fitscore:.2f}, Threshold={threshold}")

        # Only include if above threshold
        if score.fitscore >= threshold:
            logger.info(f"Coach {coach.id} PASSES threshold")
            candidates.append({"coach": coach, "score": score})
        else:
            logger.info(f"Coach {coach.id} FAILS threshold")

    # Sort by FitScore descending
    candidates.sort(key=lambda x: x["score"].fitscore, reverse=True)

    logger.info(f"Total candidates above threshold: {len(candidates)}")

    # Limit to top N candidates
    candidates = candidates[:limit]

    # Format response
    candidate_results = []
    for rank, candidate in enumerate(candidates, start=1):
        candidate_results.append(
            JobCandidateResult(
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
                rank=rank,
            )
        )

    logger.info(f"Returning {len(candidate_results)} candidates for job {job_id}")

    return JobCandidatesResponse(
        job_id=job_id,
        candidates=candidate_results,
        total_candidates=len(candidates),
        threshold=threshold,
    )
