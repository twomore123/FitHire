"""Authentication utilities for JWT validation with Clerk"""

from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import httpx

from app.config import settings

security = HTTPBearer()


async def get_clerk_jwks():
    """
    Fetch Clerk's JWKS (JSON Web Key Set) for JWT verification

    Returns:
        dict: JWKS data from Clerk
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.clerk.com/v1/jwks",
            headers={"Authorization": f"Bearer {settings.clerk_secret_key}"}
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
        unverified_header = jwt.get_unverified_header(token)

        # For now, we'll decode without verification
        # In production, you should fetch JWKS and verify the signature
        payload = jwt.decode(
            token,
            settings.clerk_secret_key,
            algorithms=["RS256"],
            options={"verify_signature": False}  # TODO: Implement proper JWKS verification
        )

        return payload

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
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
