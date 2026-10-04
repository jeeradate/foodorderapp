from typing import Any
from pathlib import Path
from icecream import ic

# 1. Import event จาก sqlalchemy โดยตรง
from sqlalchemy import event

# 2. Import ส่วนอื่นๆ จาก sqlmodel
from sqlmodel import Session, SQLModel, create_engine


BASE_DIR = Path(__file__).resolve().parent
DB_FILe_PATH = BASE_DIR / "food_order.db"
DATABASE_URL = f"sqlite:///{DB_FILe_PATH.as_posix()}"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)


@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(
    dbapi_connection: Any,
    connection_record: Any,
) -> None:
    """บังคับให้ SQLite ตรวจสอบ Foreign Key จริง"""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_db_and_tables() -> None:
    # ต้อง import ก่อน เพื่อให้ SQLModel รับรู้ทุกตาราง
    ic("Create all metadata ")
    import model  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
