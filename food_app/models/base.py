"""Base Model Helpers & Utilities

ฟังก์ชันผู้ช่วยสำหรับ Data Models เช่น การดึงเวลา UTC และ Helper สำหรับสร้าง Foreign Key
"""

from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Any, cast
from sqlmodel import Column, Field, ForeignKey, SQLModel


def th_now() -> datetime:
    """คืนค่าเวลาปัจจุบันในรูปแบบ UTC (Timezone Aware)"""
    th_tz: ZoneInfo = ZoneInfo("Asian/Bangkok")
    return datetime.now(th_tz)


def require_id(obj: SQLModel) -> int:
    """ตรวจสอบและคืนค่า primary key 'id' ของ SQLModel instance

    Raises:
        RuntimeError: หากยังไม่มีค่า id (ลืมสั่ง session.commit หรือ session.flush)
    """
    obj_id: Any = getattr(obj, "id", None)
    if obj_id is None:
        raise RuntimeError(
            f"Model {type(obj).__name__} ยังไม่มี id! คุณลืมบันทึกลง Database หรือไม่?"
        )
    return cast(int, obj_id)


def fk_column(
    target: str,
    *,
    nullable: bool = False,
    ondelete: str = "RESTRICT",
) -> Any:
    """Helper สำหรับสร้าง Foreign Key Field พร้อมกำหนด RESTRICT/CASCADE ได้สะดวก"""
    return Field(
        default=None if nullable else ...,
        sa_column=Column(
            ForeignKey(target, ondelete=ondelete),
            nullable=nullable,
        ),
    )
