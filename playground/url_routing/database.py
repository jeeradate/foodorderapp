# database.py

from pathlib import Path

from sqlmodel import SQLModel, create_engine


# ============================================================
# ตำแหน่งไฟล์ SQLite Database
# ============================================================

# Path ของโฟลเดอร์ที่เก็บไฟล์ database.py
# ตัวอย่าง:
# D:\foodorderapp\playground\foodmenu
BASE_DIR = Path(__file__).resolve().parent

# ให้เก็บ database ไว้ใน:
# foodmenu/data/food_order.db
DATABASE_PATH = BASE_DIR / "data" / "food_order.db"

# สร้างโฟลเดอร์ data อัตโนมัติ หากยังไม่มี
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

# SQLite URL:
# ใช้ as_posix() เพื่อเปลี่ยน path Windows จาก \ เป็น /
# ตัวอย่าง: sqlite:///D:/foodorderapp/playground/foodmenu/data/food_order.db
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"


# ============================================================
# สร้าง SQLModel Engine
# ============================================================

# check_same_thread=False:
# เหมาะเมื่อใช้ SQLite ร่วมกับ web application เช่น NiceGUI
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# ============================================================
# สร้าง Database Tables
# ============================================================


def create_db_and_tables() -> None:
    """
    สร้างไฟล์ SQLite และตารางทั้งหมดที่ประกาศด้วย SQLModel

    ต้อง import models ก่อน เพื่อให้ SQLModel.metadata
    รู้จัก Category และ FoodItem ก่อนสั่ง create_all()
    """
    from models import Category, FoodItem  # noqa: F401

    SQLModel.metadata.create_all(engine)
