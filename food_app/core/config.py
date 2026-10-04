"""
Configuration module for Food Order App.

Handles environment variables, application metadata, and database configuration settings.
Uses Pydantic BaseSettings for type validation and environment variable parsing.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings class using Pydantic BaseSettings.

    Reads default configuration parameters or overrides them using environment variables (.env).
    """

    # Application Information
    APP_TITLE: str = "Food Order App"
    APP_VERSION: str = "0.1.0"

    # Server & Environment Settings
    HOST: str = "127.0.0.1"
    PORT: int = 8080
    DEBUG_MODE: bool = True

    # Base Directory Structure
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    # Database Configuration (SQLite default for local development)
    DATABASE_FILE: str = "food_order_app.db"

    @property
    def DATABASE_URL(self) -> str:
        """Dynamically constructs SQLite database URL connection string.

        Returns:
            str: Connection string for SQLModel engine.
        """
        db_path: Path = self.BASE_DIR / self.DATABASE_FILE
        return f"sqlite:///{db_path}"

    # Pydantic Configuration to support .env file loading
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Instantiate single configuration instance for globally shared access
settings: Settings = Settings()
