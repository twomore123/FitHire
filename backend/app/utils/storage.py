"""File storage utilities for Cloudflare R2"""

import uuid
import io
from typing import BinaryIO, Optional
import boto3
from botocore.exceptions import ClientError
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class R2Storage:
    """Cloudflare R2 storage client using S3-compatible API"""

    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url=settings.r2_endpoint,
            aws_access_key_id=settings.r2_access_key_id,
            aws_secret_access_key=settings.r2_secret_access_key,
            region_name='auto',  # R2 uses 'auto' for region
        )
        self.bucket_name = settings.r2_bucket_name
        self.public_url = settings.r2_public_url

    def upload_file(
        self,
        file: bytes,
        filename: str,
        content_type: str,
        folder: str = "uploads"
    ) -> str:
        """
        Upload a file to R2 storage

        Args:
            file: File bytes to upload
            filename: Original filename
            content_type: MIME type (e.g., 'image/jpeg')
            folder: Folder path in bucket (e.g., 'profile-pictures', 'brand-logos')

        Returns:
            str: Public URL of the uploaded file
        """
        try:
            # Generate unique filename to avoid conflicts
            extension = filename.rsplit('.', 1)[-1] if '.' in filename else ''
            unique_filename = f"{uuid.uuid4()}.{extension}" if extension else str(uuid.uuid4())
            key = f"{folder}/{unique_filename}"

            # Convert bytes to file-like object
            file_obj = io.BytesIO(file)

            # Upload to R2
            self.client.upload_fileobj(
                file_obj,
                self.bucket_name,
                key,
                ExtraArgs={
                    'ContentType': content_type,
                    'CacheControl': 'public, max-age=31536000',  # Cache for 1 year
                }
            )

            # Generate public URL
            if self.public_url:
                url = f"{self.public_url}/{key}"
            else:
                # Fallback to R2 endpoint URL
                url = f"{self.r2_endpoint}/{self.bucket_name}/{key}"

            logger.info(f"Uploaded file to R2: {key}")
            return url

        except ClientError as e:
            logger.error(f"Failed to upload file to R2: {str(e)}")
            raise Exception(f"File upload failed: {str(e)}")

    def delete_file(self, url: str) -> bool:
        """
        Delete a file from R2 storage

        Args:
            url: Public URL of the file to delete

        Returns:
            bool: True if successful
        """
        try:
            # Extract key from URL
            if self.public_url and url.startswith(self.public_url):
                key = url.replace(f"{self.public_url}/", "")
            else:
                # Try to extract from endpoint URL
                key = url.split(f"{self.bucket_name}/")[-1]

            self.client.delete_object(Bucket=self.bucket_name, Key=key)
            logger.info(f"Deleted file from R2: {key}")
            return True

        except ClientError as e:
            logger.error(f"Failed to delete file from R2: {str(e)}")
            return False


# Singleton instance
_storage_client: Optional[R2Storage] = None


def get_storage_client() -> R2Storage:
    """Get or create R2 storage client singleton"""
    global _storage_client
    if _storage_client is None:
        _storage_client = R2Storage()
    return _storage_client
