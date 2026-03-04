"""Coach CRUD and matching endpoints"""

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
from app.schemas.coach import CoachCreate, CoachListResponse, CoachResponse, CoachUpdate
from app.schemas.match import CoachMatchesResponse, CoachMatchResult, FitScoreBreakdown
from app.utils.auth import get_current_user

router = APIRouter(prefix="/coaches", tags=["coaches"])
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
                role="coach",  # Default role for new users
                # brand_id intentionally omitted - nullable, assigned later via coach/location
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


def calculate_profile_completeness(coach_data: dict) -> float:
    """
    Calculate profile completeness percentage

    Core fields (required for 100%):
    - bio
    - certifications (at least one)
    - available_times (at least one)
    - coaching style tags (at least one type)

    Optional media fields don't affect core completeness.
    Profile can reach 100% without photo/video.
    """
    total_fields = 4
    completed = 0

    if coach_data.get("bio"):
        completed += 1
    if coach_data.get("certifications") and len(coach_data["certifications"]) > 0:
        completed += 1
    if coach_data.get("available_times") and len(coach_data["available_times"]) > 0:
        completed += 1
    if (
        coach_data.get("lifestyle_tags")
        or coach_data.get("movement_tags")
        or coach_data.get("instruction_tags")
    ):
        completed += 1

    return round(completed / total_fields, 2)


@router.post("/", response_model=CoachResponse, status_code=status.HTTP_201_CREATED)
async def create_coach(
    coach_data: CoachCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Create a new coach profile

    Requires authentication. Users can only create coaches in their authorized locations.
    """
    # Verify location exists and user has access
    location = db.query(Location).filter(Location.id == coach_data.location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location {coach_data.location_id} not found",
        )

    # Get or create user from Clerk authentication
    user = get_or_create_user(db, current_user)

    # Check if coach already exists for this user
    existing_coach = db.query(Coach).filter(Coach.user_id == user.id).first()
    if existing_coach:
        # Update existing coach instead of creating new one
        existing_coach.brand_id = location.brand_id
        existing_coach.city = coach_data.city
        existing_coach.state = coach_data.state
        existing_coach.bio = coach_data.bio
        existing_coach.years_experience = coach_data.years_experience
        existing_coach.certifications = [cert.model_dump() for cert in coach_data.certifications]
        existing_coach.available_times = coach_data.available_times
        existing_coach.lifestyle_tags = coach_data.lifestyle_tags
        existing_coach.movement_tags = coach_data.movement_tags
        existing_coach.instruction_tags = coach_data.instruction_tags
        existing_coach.profile_image_url = (
            str(coach_data.profile_photo_url) if coach_data.profile_photo_url else None
        )
        existing_coach.verified_video_url = (
            str(coach_data.verified_video_url) if coach_data.verified_video_url else None
        )
        existing_coach.profile_completeness = calculate_profile_completeness(
            coach_data.model_dump()
        )
        existing_coach.last_updated = datetime.now()
        existing_coach.verified_at = datetime.now()  # Auto-verify for Phase 1 testing

        db.commit()
        db.refresh(existing_coach)
        return existing_coach

    # Calculate profile completeness
    completeness = calculate_profile_completeness(coach_data.model_dump())

    # Create coach (only set fields that exist in Coach model)
    new_coach = Coach(
        user_id=user.id,
        brand_id=location.brand_id,
        city=coach_data.city,
        state=coach_data.state,
        bio=coach_data.bio,
        years_experience=coach_data.years_experience,
        certifications=[cert.model_dump() for cert in coach_data.certifications],
        available_times=coach_data.available_times,
        lifestyle_tags=coach_data.lifestyle_tags,
        movement_tags=coach_data.movement_tags,
        instruction_tags=coach_data.instruction_tags,
        profile_image_url=(
            str(coach_data.profile_photo_url) if coach_data.profile_photo_url else None
        ),
        verified_video_url=(
            str(coach_data.verified_video_url) if coach_data.verified_video_url else None
        ),
        profile_completeness=completeness,
        last_updated=datetime.now(),
        verified_at=datetime.now(),  # Auto-verify for Phase 1 testing
    )

    db.add(new_coach)
    db.commit()
    db.refresh(new_coach)

    return new_coach


@router.get("/{coach_id}", response_model=CoachResponse)
async def get_coach(
    coach_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    """
    Get a single coach profile by ID

    Requires authentication. Users can only view their own coach profiles.
    """
    # Get the current user from database
    user = get_or_create_user(db, current_user)

    coach = db.query(Coach).filter(Coach.id == coach_id).first()
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Coach {coach_id} not found"
        )

    # Verify that this coach belongs to the current user
    # (Managers and admins viewing candidates will use the matches endpoint)
    if coach.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this coach profile",
        )

    return coach


@router.get("/", response_model=CoachListResponse)
async def list_coaches(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    location_id: Optional[int] = Query(None, description="Filter by location"),
    role_type: Optional[str] = Query(None, description="Filter by role type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    List coaches with pagination and filtering

    Requires authentication. Users see only their own coach profiles.
    """
    # Get the current user from database
    user = get_or_create_user(db, current_user)

    # Start with query filtered by current user
    query = db.query(Coach).filter(Coach.user_id == user.id)

    # Apply additional filters
    # Filter by verified coaches only if status filter is requested
    if status == "verified":
        query = query.filter(Coach.verified_at.isnot(None))
    elif status == "unverified":
        query = query.filter(Coach.verified_at.is_(None))

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * page_size
    coaches = query.order_by(Coach.created_at.desc()).offset(offset).limit(page_size).all()

    return CoachListResponse(
        coaches=coaches,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.patch("/{coach_id}", response_model=CoachResponse)
async def update_coach(
    coach_id: int,
    coach_update: CoachUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update a coach profile

    Requires authentication. Users can only update their own coach profiles.
    """
    # Get the current user from database
    user = get_or_create_user(db, current_user)

    # Fetch the coach and verify ownership
    coach = db.query(Coach).filter(Coach.id == coach_id).first()
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Coach {coach_id} not found"
        )

    # Verify that this coach belongs to the current user
    if coach.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this coach profile",
        )

    # Update fields if provided (only fields that exist in Coach model)
    update_data = coach_update.model_dump(exclude_unset=True)

    # Map frontend field names to Coach model field names
    field_mapping = {
        "profile_photo_url": "profile_image_url",  # Frontend uses profile_photo_url, model uses profile_image_url
    }

    for field, value in update_data.items():
        # Map field names
        model_field = field_mapping.get(field, field)

        if field == "certifications" and value is not None:
            # Handle both Pydantic models and plain dicts from frontend
            certs = []
            for cert in value:
                if isinstance(cert, dict):
                    certs.append(cert)  # Already a dict
                else:
                    certs.append(cert.model_dump())  # Pydantic model
            setattr(coach, model_field, certs)
        elif field in ["profile_photo_url", "verified_video_url"] and value is not None:
            # Convert HttpUrl to string
            setattr(coach, model_field, str(value) if value else None)
        else:
            setattr(coach, model_field, value)

    # Recalculate profile completeness (only using fields that exist in Coach model)
    coach_dict = {
        "bio": coach.bio,
        "certifications": coach.certifications,
        "years_experience": coach.years_experience,
        "available_times": coach.available_times,
        "profile_image_url": coach.profile_image_url,
        "verified_video_url": coach.verified_video_url,
        "lifestyle_tags": coach.lifestyle_tags,
        "movement_tags": coach.movement_tags,
        "instruction_tags": coach.instruction_tags,
    }
    coach.profile_completeness = calculate_profile_completeness(coach_dict)

    # Update last_updated timestamp and auto-verify for Phase 1
    coach.last_updated = datetime.now()
    coach.verified_at = datetime.now()  # Auto-verify on update for Phase 1 testing

    db.commit()
    db.refresh(coach)

    return coach


@router.get("/{coach_id}/matches", response_model=CoachMatchesResponse)
async def get_coach_matches(
    coach_id: int,
    limit: int = Query(20, ge=1, le=20, description="Maximum number of matches to return"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Get top job matches for a coach

    Returns jobs ranked by FitScore, filtered by the job's threshold.
    Only returns jobs with status='open'.
    """
    # Get the current user from database
    user = get_or_create_user(db, current_user)

    # Get coach and verify ownership
    coach = db.query(Coach).filter(Coach.id == coach_id).first()
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Coach {coach_id} not found"
        )

    # Verify that this coach belongs to the current user
    if coach.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view matches for this coach profile",
        )

    # Get all open jobs in the same city (Phase 1: exact city match only)
    jobs = (
        db.query(Job)
        .filter(and_(Job.is_active, Job.city == coach.city, Job.state == coach.state))
        .all()
    )

    # Calculate FitScore for each job
    engine = FitScoreEngine()
    matches = []

    # Prepare coach data for FitScore engine
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

    for job in jobs:
        job_data = {
            "required_certifications": job.required_certifications,
            "preferred_certifications": job.preferred_certifications,
            "min_experience": job.min_experience,
            "required_availability": job.required_availability,
            "city": job.city,
            "state": job.state,
            "culture_tags": job.culture_tags,
        }

        score = engine.calculate_match(
            coach_data, job_data, preset=job.weighting_preset, custom_weights=job.custom_weights
        )

        # Only include if above threshold
        threshold = float(job.fitscore_threshold) if job.fitscore_threshold else 0.60
        if score.fitscore >= threshold:
            matches.append({"job": job, "score": score, "threshold": threshold})

    # Sort by FitScore descending
    matches.sort(key=lambda x: x["score"].fitscore, reverse=True)

    # Limit to top N matches
    matches = matches[:limit]

    # Format response
    match_results = []
    for rank, match in enumerate(matches, start=1):
        match_results.append(
            CoachMatchResult(
                job=match["job"],
                fitscore=match["score"].fitscore,
                score_breakdown=FitScoreBreakdown(
                    fitscore=match["score"].fitscore,
                    cert_score=match["score"].cert_score,
                    experience_score=match["score"].experience_score,
                    availability_score=match["score"].availability_score,
                    location_score=match["score"].location_score,
                    culture_score=match["score"].culture_score,
                    engagement_score=match["score"].engagement_score,
                ),
                rank=rank,
            )
        )

    return CoachMatchesResponse(
        coach_id=coach_id,
        matches=match_results,
        total_matches=len(matches),
        threshold=0.60,  # Default threshold for display
    )
