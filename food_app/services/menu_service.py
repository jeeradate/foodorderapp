"""Menu Service Module

ให้บริการจัดการการดึงข้อมูลและเพิ่มข้อมูลเมนูอาหารสำหรับ UI Layer
"""

from decimal import Decimal
from typing import Any, Optional
from sqlmodel import Session, select

from food_app.core.database import engine
from food_app.models.master import Category, Menu


def get_all_categories() -> list[dict[str, Any]]:
    """ดึงข้อมูลหมวดหมู่ทั้งหมด"""
    with Session(engine) as session:
        statement = select(Category).where(Category.is_active)
        categories = session.exec(statement).all()
        return [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
            }
            for c in categories
        ]


def create_sample_data_if_empty() -> None:
    """สร้างข้อมูลตัวอย่าง หากในระบบยังไม่มีข้อมูล"""
    with Session(engine) as session:
        existing_cat = session.exec(select(Category)).first()
        if existing_cat is None:
            cat_main = Category(name="อาหารจานเดียว", description="เมนูผัด/ราดข้าว")
            cat_drink = Category(name="เครื่องดื่ม", description="น้ำดื่มและน้ำหวาน")
            session.add(cat_main)
            session.add(cat_drink)
            session.commit()

            session.refresh(cat_main)
            session.refresh(cat_drink)

            m1 = Menu(
                category_id=cat_main.id,  # type: ignore
                name="กระเพราหมูกรอบ",
                base_price=Decimal("65.00"),
            )
            m2 = Menu(
                category_id=cat_drink.id,  # type: ignore
                name="ชาไทยเย็น",
                base_price=Decimal("35.00"),
            )
            session.add(m1)
            session.add(m2)
            session.commit()


def get_menus_by_category(category_id: Optional[int] = None) -> list[dict[str, Any]]:
    """ดึงข้อมูลรายการอาหารตามหมวดหมู่"""
    with Session(engine) as session:
        statement = select(Menu).where(Menu.is_active)
        if category_id is not None:
            statement = statement.where(Menu.category_id == category_id)

        menus = session.exec(statement).all()
        return [
            {
                "id": m.id,
                "name": m.name,
                "base_price": float(m.base_price),
            }
            for m in menus
        ]
