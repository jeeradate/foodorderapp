# database.py

from pathlib import Path

from sqlmodel import SQLModel, create_engine


# __file__ คือ path ของไฟล์ database.py
# .resolve() แปลงเป็น absolute path
# .parent คือ folder ที่เก็บ database.py
BASE_DIR = Path(__file__).resolve().parent

# กำหนดตำแหน่ง database:
# D:\foodorderapp\playground\foodmenu\data\food_order.db
DATABASE_PATH = BASE_DIR / "data" / "food_order.db"

# สร้างโฟลเดอร์ data หากยังไม่มี
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

# as_posix() แปลง \ เป็น / เพื่อให้ใช้กับ SQLite URL ได้แน่นอน
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables() -> None:
    """สร้าง database และ tables หากยังไม่มี"""
    SQLModel.metadata.create_all(engine)
