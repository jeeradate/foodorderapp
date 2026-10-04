"""
Module: food_app.core.config
Description: Configuration settings for Food Order App using Pydantic / Environment Settings.
"""

import os
from typing import Final


class Settings:
    """Class สำหรับจัดการค่า Configuration ของ Application"""

    APP_TITLE: Final[str] = "Food Order App"
    HOST: Final[str] = os.getenv("HOST", "127.0.0.1")
    PORT: Final[int] = int(os.getenv("PORT", "8080"))

    # เช็กว่าอยู่ในสถานะ Development หรือไม่ (Default เป็น True ถ้าไม่ได้กำหนด)
    DEBUG_MODE: Final[bool] = os.getenv("DEBUG_MODE", "True").lower() in (
        "true",
        "1",
        "t",
    )


# Export Instance ของ Settings เพื่อนำไปใช้งานในโมดูลอื่น
settings: Final[Settings] = Settings()
