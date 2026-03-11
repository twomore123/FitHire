"""File upload endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import Literal
import logging

from app.utils.auth import get_current_user
from app.utils.storage import get_storage_client

router = APIRouter(prefix="/upload", tags=["upload"])
logger = logging.getLogger(__name__)

# Allowed image types
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    folder: Literal["profile-pictures", "brand-logos", "brand-banners"] = "profile-pictures",
    current_user: dict = Depends(get_current_user)
):
    """
    Upload an image file to R2 storage

    Args:
        file: Image file to upload
        folder: Storage folder (profile-pictures, brand-logos, brand-banners)
        current_user: Authenticated user

    Returns:
        dict: Upload result with public URL
    """
    # Validate file type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )

    # Read file content
    content = await file.read()

    # Validate file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024 * 1024)}MB"
        )

    try:
        # Upload to R2
        storage = get_storage_client()
        url = storage.upload_file(
            file=content,
            filename=file.filename or "upload",
            content_type=file.content_type,
            folder=folder
        )

        logger.info(f"User {current_user.get('sub')} uploaded image to {folder}: {url}")

        return {
            "success": True,
            "url": url,
            "filename": file.filename,
            "content_type": file.content_type,
            "folder": folder
        }

    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Upload failed. Please try again."
        )


@router.delete("/image")
async def delete_image(
    url: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete an image from R2 storage

    Args:
        url: Public URL of the image to delete
        current_user: Authenticated user

    Returns:
        dict: Deletion result
    """
    try:
        storage = get_storage_client()
        success = storage.delete_file(url)

        if success:
            logger.info(f"User {current_user.get('sub')} deleted image: {url}")
            return {"success": True, "message": "Image deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )

    except Exception as e:
        logger.error(f"Delete failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Delete failed. Please try again."
        )
