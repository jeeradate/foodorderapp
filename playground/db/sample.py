from typing import List, Optional
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from pathlib import Path
from icecream import ic

ic("Start====================")


CurentDir: Path = Path(__file__).resolve().parent
ic(CurentDir)


# ==========================================
# 1. MODEL DEFINITIONS (นิยามโครงสร้างตาราง)
# ==========================================


class Category(SQLModel, table=True):
    """ตารางฝั่ง ONE (1 หมวดหมู่ มีได้หลายรายการอาหาร)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)

    # Relationship: เชื่อมไปยัง FoodItem
    items: List["FoodItem"] = Relationship(back_populates="category")


class FoodItem(SQLModel, table=True):
    """ตารางฝั่ง MANY (หลายรายการอาหาร อยู่ใน 1 หมวดหมู่)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: float = Field(gt=0)

    # [FIXED]: ปรับเป็น Optional[int] = Field(default=None, ...) เพื่อให้ Type Checker รู้ว่าไม่ต้องส่งค่ามาตอนสร้าง Object ได้
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")

    # Relationship: อ้างอิงกลับไปยังวัตถุ Category
    category: Optional[Category] = Relationship(back_populates="items")


# ==========================================
# 2. DATABASE SETUP (ตั้งค่าฐานข้อมูล SQLite)
# ==========================================

sqlite_file_name: str = "database.db"
ic(sqlite_file_name)
sqlite_url: str = f"sqlite:///{CurentDir}/{sqlite_file_name}"
ic(sqlite_url)
engine = create_engine(sqlite_url, echo=False)
ic(engine)


def create_db_and_tables() -> None:
    """สร้างตารางใน Database ตาม Models ที่นิยามไว้"""
    SQLModel.metadata.create_all(engine)


# ==========================================
# 3. CRUD OPERATIONS (ทดลองทำ C-R-U-D)
# ==========================================


def create_data() -> None:
    """สร้างหมวดหมู่พร้อมรายการอาหาร"""
    with Session(engine) as session:
        cat_beverage = Category(name="Beverage")
        cat_food = Category(name="Main Dishes")

        # บรรทัดเหล่านี้จะไม่มี Pylance warning อีกต่อไป
        item1 = FoodItem(name="Iced Green Tea", price=55.0, category=cat_beverage)
        item2 = FoodItem(name="Espresso", price=50.0, category=cat_beverage)
        item3 = FoodItem(name="Pad Thai", price=80.0, category=cat_food)

        session.add(cat_beverage)
        session.add(cat_food)
        session.add(item1)
        session.add(item2)
        session.add(item3)

        session.commit()
        print("✅ [CREATE] Data added successfully!")


def read_data() -> None:
    """อ่านข้อมูลและดึงความสัมพันธ์ 1-to-Many"""
    with Session(engine) as session:
        print("\n--- [READ 1] List all categories with their items ---")
        statement = select(Category)
        categories = session.exec(statement).all()

        for cat in categories:
            print(f"Category: {cat.name} (ID: {cat.id})")
            for item in cat.items:
                print(f"  └─ Food: {item.name} | Price: ฿{item.price}")

        print("\n--- [READ 2] List food items with their parent category ---")
        statement_food = select(FoodItem)
        foods = session.exec(statement_food).all()

        for food in foods:
            cat_name = food.category.name if food.category else "Unknown"
            print(f"Food: {food.name} -> Category: {cat_name}")


def update_data() -> None:
    """แก้ไขข้อมูลราคา และเปลี่ยนหมวดหมู่อาหาร"""
    with Session(engine) as session:
        statement = select(FoodItem).where(FoodItem.name == "Espresso")
        espresso = session.exec(statement).first()

        if espresso:
            old_price = espresso.price
            espresso.price = 60.0

            session.add(espresso)
            session.commit()
            session.refresh(espresso)
            print(
                f"\n✅ [UPDATE] Updated {espresso.name} price from ฿{old_price} to ฿{espresso.price}"
            )


def delete_data() -> None:
    """ลบรายการอาหาร"""
    with Session(engine) as session:
        statement = select(FoodItem).where(FoodItem.name == "Pad Thai")
        pad_thai = session.exec(statement).first()

        if pad_thai:
            session.delete(pad_thai)
            session.commit()
            # [FIXED]: เอา f ออกจาก string ที่ไม่มี placeholder
            print("\n✅ [DELETE] Deleted food item: Pad Thai")


if __name__ == "__main__":
    create_db_and_tables()
    create_data()
    read_data()
    update_data()
    delete_data()

    print("\n--- [READ AFTER DELETE] Current Data ---")
    read_data()
