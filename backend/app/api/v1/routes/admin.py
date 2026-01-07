"""Admin verification and management endpoints"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.coach import Coach
from app.schemas.coach import CoachResponse
from app.utils.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/verification-queue", response_model=List[CoachResponse])
async def get_verification_queue(
    db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    """
    Get list of coaches pending verification

    Returns coaches where verified_at is NULL
    Requires admin role (TODO: add role check)
    """
    # TODO: Add admin role check
    # if current_user.get("role") != "admin":
    #     raise HTTPException(status_code=403, detail="Admin access required")

    # Get all unverified coaches
    pending_coaches = (
        db.query(Coach).filter(Coach.verified_at.is_(None)).order_by(Coach.created_at.desc()).all()
    )

    return pending_coaches


@router.post("/verify-coach/{coach_id}", response_model=CoachResponse)
async def verify_coach(
    coach_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    """
    Approve and verify a coach profile

    Sets verified_at timestamp to current time
    Requires admin role (TODO: add role check)
    """
    # TODO: Add admin role check
    # if current_user.get("role") != "admin":
    #     raise HTTPException(status_code=403, detail="Admin access required")

    # Get coach
    coach = db.query(Coach).filter(Coach.id == coach_id).first()
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Coach {coach_id} not found"
        )

    # Verify coach
    coach.verified_at = datetime.now()

    db.commit()
    db.refresh(coach)

    return coach


@router.post("/reject-coach/{coach_id}")
async def reject_coach(
    coach_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    """
    Reject a coach profile verification

    For Phase 1, this just unsets verified_at
    Phase 2+ can add rejection reasons, notifications, etc.
    Requires admin role (TODO: add role check)
    """
    # TODO: Add admin role check
    # if current_user.get("role") != "admin":
    #     raise HTTPException(status_code=403, detail="Admin access required")

    # Get coach
    coach = db.query(Coach).filter(Coach.id == coach_id).first()
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Coach {coach_id} not found"
        )

    # Unset verification
    coach.verified_at = None

    db.commit()

    return {"message": f"Coach {coach_id} verification rejected", "coach_id": coach_id}
