"""Application configuration using Pydantic Settings"""

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    environment: str = Field(default="development", description="Environment: development, staging, production")
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_reload: bool = Field(default=True, description="Enable auto-reload for development")
    secret_key: str = Field(..., description="Secret key for JWT signing")

    # CORS
    cors_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000",
        description="Allowed CORS origins (comma-separated)"
    )

    # Database
    database_url: str = Field(..., description="PostgreSQL connection string")
    db_pool_size: int = Field(default=10, description="Database connection pool size")
    db_max_overflow: int = Field(default=20, description="Max database connections overflow")
    db_pool_timeout: int = Field(default=30, description="Database pool timeout in seconds")

    # Clerk Authentication
    clerk_secret_key: str = Field(..., description="Clerk secret key")
    clerk_publishable_key: str = Field(..., description="Clerk publishable key")
    clerk_webhook_secret: str = Field(..., description="Clerk webhook signing secret")

    # Cloudflare R2
    r2_account_id: str = Field(..., description="Cloudflare account ID")
    r2_bucket_name: str = Field(default="fithire", description="R2 bucket name")
    r2_access_key_id: str = Field(..., description="R2 access key ID")
    r2_secret_access_key: str = Field(..., description="R2 secret access key")
    r2_endpoint: str = Field(..., description="R2 S3-compatible endpoint")
    r2_public_url: str = Field(default="", description="Public CDN URL for R2 bucket")

    # Redis (Phase 2)
    redis_url: str = Field(default="redis://localhost:6379/0", description="Redis connection string")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format: json or text")

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.environment == "production"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Using lru_cache ensures Settings is instantiated only once,
    improving performance and preventing multiple env file reads.
    """
    return Settings()


# Convenience export
settings = get_settings()
