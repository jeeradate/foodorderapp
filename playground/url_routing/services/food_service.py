# services/food_service.py

from sqlmodel import Session, select

from database import engine
from models import Category, FoodItem


def get_categories() -> list[Category]:
    """ดึง Category ทั้งหมดจาก database"""
    with Session(engine) as session:
        statement = select(Category).order_by(Category.name)
        return list(session.exec(statement).all())


def get_category_options() -> dict[int, str]:
    """
    สร้างข้อมูลสำหรับ ui.select

    ตัวอย่าง:
    {1: "อาหารจานเดียว", 2: "เครื่องดื่ม"}
    """
    return {
        category.id: category.name
        for category in get_categories()
        if category.id is not None
    }


def get_food_items_by_category(category_id: int) -> list[FoodItem]:
    """ดึง Food Item เฉพาะ Category ที่เลือก"""
    with Session(engine) as session:
        statement = (
            select(FoodItem)
            .where(FoodItem.category_id == category_id)
            .order_by(FoodItem.name)
        )
        return list(session.exec(statement).all())


def add_category(name: str) -> None:
    """เพิ่ม Category ใหม่"""
    with Session(engine) as session:
        category = Category(name=name)
        session.add(category)
        session.commit()


def add_food_item(name: str, price: float, category_id: int) -> None:
    """เพิ่มรายการอาหารใหม่"""
    with Session(engine) as session:
        food_item = FoodItem(
            name=name,
            price=price,
            category_id=category_id,
        )
        session.add(food_item)
        session.commit()
