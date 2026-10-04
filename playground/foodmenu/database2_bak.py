# AI  เขียนให้ มี comment
from pathlib import Path
from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine

# 1. หา Absolute Path ของ Directory ปัจจุบันที่ไฟล์นี้ตั้งอยู่
BASE_DIR: Path = Path(__file__).resolve().parent

# 2. กำหนด Path ของไฟล์ Database (สร้างโฟลเดอร์ data อัตโนมัติถ้ายังไม่มี)
DATABASE_PATH: Path = BASE_DIR / "data" / "food_order2.db"
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

# 3. แปลง Path เป็น URL Format สำหรับ SQLite (ใช้ as_posix() เพื่อรองรับ Slash / ในทุก OS)
DATABASE_URL: str = f"sqlite:///{DATABASE_PATH.as_posix()}"

# 4. สร้าง Database Engine
engine: Engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_db_data_tables() -> None:
    """สร้างตารางข้อมูลใน Database ตาม Models ที่นิยามไว้"""
    SQLModel.metadata.create_all(engine)
