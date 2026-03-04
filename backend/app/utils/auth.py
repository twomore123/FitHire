"""Authentication utilities for JWT validation with Clerk"""

import logging

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.db.session import get_db
from app.models.user import User

logger = logging.getLogger(__name__)

security = HTTPBearer()


async def get_clerk_jwks():
    """
    Fetch Clerk's JWKS (JSON Web Key Set) for JWT verification

    Returns:
        dict: JWKS data from Clerk
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.clerk.com/v1/jwks",
            headers={"Authorization": f"Bearer {settings.clerk_secret_key}"},
        )
        response.raise_for_status()
        return response.json()


async def verify_jwt_token(token: str) -> dict:
    """
    Verify JWT token from Clerk

    Args:
        token: JWT token string

    Returns:
        dict: Decoded token payload with user claims

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Decode without verification first to get the header
        jwt.get_unverified_header(token)

        # For now, we'll decode without verification
        # In production, you should fetch JWKS and verify the signature
        payload = jwt.decode(
            token,
            settings.clerk_secret_key,
            algorithms=["RS256"],
            options={"verify_signature": False},  # TODO: Implement proper JWKS verification
        )

        return payload

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Dependency function to get the current authenticated user

    Args:
        credentials: HTTP Bearer token from request header

    Returns:
        dict: User claims from JWT token

    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    return await verify_jwt_token(token)


def get_current_user_db(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> User:
    """
    FastAPI dependency that resolves the current authenticated user
    to a database User record. Creates the record if it doesn't exist.

    Args:
        db: Database session (injected by FastAPI)
        current_user: Decoded JWT payload from Clerk (injected by FastAPI)

    Returns:
        User: The database user record
    """
    clerk_user_id = current_user.get("sub")
    logger.info(f"JWT payload keys: {list(current_user.keys())}")
    logger.info(f"Clerk user ID: {clerk_user_id}")

    if not clerk_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token: missing user ID",
        )

    user = db.query(User).filter(User.clerk_user_id == clerk_user_id).first()

    if not user:
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
            role="coach",
            brand_id=1,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"Created user with ID: {user.id}")
    else:
        logger.info(f"Found existing user with ID: {user.id}")

    return user


def require_role(*allowed_roles: str):
    """
    Dependency factory for role-based access control

    Usage:
        @app.get("/admin/users", dependencies=[Depends(require_role("brand_admin"))])

    Args:
        *allowed_roles: Variable number of allowed role names

    Returns:
        Dependency function that checks user role
    """

    async def role_checker(user: dict = Depends(get_current_user)) -> dict:
        user_role = user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {', '.join(allowed_roles)}",
            )
        return user

    return role_checker
