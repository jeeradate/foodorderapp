"""Configuration module for Food Order App.

Handles environment variables, application metadata, and database connection settings.
Supports dynamic environment binding for local SQLite and cloud-hosted PostgreSQL (Supabase/Render).
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings class managed via Pydantic BaseSettings.

    Reads configuration parameters from environment variables or falls back to default values.
    """

    # Application Information
    APP_TITLE: str = "Food Order App"
    APP_VERSION: str = "0.1.0"

    # Server Configuration (Render dynamically assigns PORT)
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8080"))
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "True").lower() in ("true", "1", "t")

    # Directory Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    # Database Configuration
    DATABASE_URL_ENV: Optional[str] = os.getenv("DATABASE_URL")
    DATABASE_FILE: str = "food_order_app.db"

    @property
    def DATABASE_URL(self) -> str:
        """Dynamically computes SQLModel database connection URL.

        If DATABASE_URL environment variable is present (e.g. Supabase PostgreSQL), it returns that URL.
        Otherwise, it falls back to local SQLite file database.

        Returns:
            str: Connection string formatted for SQLAlchemy/SQLModel engine.
        """
        if self.DATABASE_URL_ENV:
            # Fix legacy 'postgres://' scheme to 'postgresql://' for SQLAlchemy 2.0 compatibility
            if self.DATABASE_URL_ENV.startswith("postgres://"):
                return self.DATABASE_URL_ENV.replace("postgres://", "postgresql://", 1)
            return self.DATABASE_URL_ENV

        db_path: Path = self.BASE_DIR / self.DATABASE_FILE
        return f"sqlite:///{db_path}"

    # Configuration for loading .env file locally
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Instantiate globally accessible settings instance
settings: Settings = Settings()
