"""Database Core Configuration Module

โมดูลจัดการการเชื่อมต่อฐานข้อมูล SQLite ร่วมกับ SQLModel
พร้อมการตั้งค่า Event Listener เพื่อเปิดใช้งาน Foreign Key Constraint ใน SQLite
"""

from pathlib import Path
from typing import Any, Generator

from sqlalchemy import event
from sqlmodel import Session, SQLModel, create_engine

# กำหนด Path สำหรับไฟล์ฐานข้อมูลให้อยู่ที่ Root ของโปรเจกต์
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
DB_FILE_PATH: Path = BASE_DIR / "food_order.db"
DATABASE_URL: str = f"sqlite:///{DB_FILE_PATH.as_posix()}"

# สร้าง Database Engine
# check_same_thread=False จำเป็นต้องใส่เมื่อใช้งานร่วมกับ Web Framework/NiceGUI
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)


@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection: Any, connection_record: Any) -> None:
    """บังคับให้ SQLite ตรวจสอบ Foreign Key Constraints ทุกครั้งที่มี Connection ใหม่"""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()


def create_db_and_tables() -> None:
    """สร้างตารางในฐานข้อมูลตาม Model ทั้งหมดที่ลงทะเบียนไว้"""
    import food_app.models  # noqa: F401 (Import เพื่อให้ SQLModel รู้จักตาราง)

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Generator Function สำหรับจัดการ Database Session"""
    with Session(engine) as session:
        yield session
