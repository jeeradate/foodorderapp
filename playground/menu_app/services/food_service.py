from typing import Optional
from sqlmodel import Session, select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from database import engine
from models import Category, FoodItem, FoodOption


def get_categories() -> list[Category]:
    """ดึงข้อมูลหมวดหมู่อาหารทั้งหมด เรียงตามชื่อ"""
    with Session(engine) as session:
        statement: SelectOfScalar[Category] = select(Category).order_by(Category.name)
        return list(session.exec(statement).all())


def get_category_options() -> dict[int, str]:
    """แปลงข้อมูล Category เป็น Dictionary {id: name} สำหรับ ui.select"""
    return {
        category.id: category.name
        for category in get_categories()
        if category.id is not None
    }


def get_food_item_by_category(category_id: int) -> list[FoodItem]:
    """ดึงรายการอาหารพร้อมตัวเลือกเสริม (FoodOptions) ตาม Category ID"""
    with Session(engine) as session:
        statement: SelectOfScalar[FoodItem] = (
            select(FoodItem)
            .where(FoodItem.category_id == category_id)
            .order_by(FoodItem.name)
        )
        items: list[FoodItem] = list(session.exec(statement).all())

        # Access relationship เพื่อให้ SQLModel โหลด options เข้ามาใน memory ก่อนปิด Session
        for item in items:
            _ = item.options

        return items


def add_category(cname: str) -> None:
    """เพิ่มหมวดหมู่อาหารใหม่"""
    with Session(engine) as session:
        category = Category(name=cname)
        session.add(category)
        session.commit()


def add_food_item_with_options(
    name: str,
    price: float,
    category_id: int,
    # แก้ไข Type Hint ตรงนี้ให้รับ Value เป็นได้ทั้ง str และ float (หรือใช้ Any)
    options_data: Optional[list[dict[str, str | float]]] = None,
) -> None:
    """เพิ่มรายการอาหารพร้อมกับตัวเลือกเสริม (Options) ในเวลาเดียวกัน"""
    with Session(engine) as session:
        food_item = FoodItem(
            name=name,
            price=price,
            category_id=category_id,
        )
        session.add(food_item)
        session.commit()
        session.refresh(food_item)

        # หากมีข้อมูลตัวเลือกเสริม ให้บันทึกเพิ่มเข้าไป
        if options_data and food_item.id is not None:
            for opt in options_data:
                # ดึงค่า name แล้วแปลงเป็น str ให้ชัดเจนเพื่อความปลอดภัย
                raw_name = opt.get("name", "")
                opt_name: str = str(raw_name).strip() if raw_name else ""

                # ดึงค่า extra_price แล้วแปลงเป็น float
                raw_price = opt.get("extra_price", 0.0)
                extra_price: float = float(raw_price) if raw_price is not None else 0.0

                if opt_name:
                    food_option = FoodOption(
                        name=opt_name,
                        extra_price=extra_price,
                        food_item_id=food_item.id,
                    )
                    session.add(food_option)
            session.commit()
