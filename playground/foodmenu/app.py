# app.py
from decimal import Decimal
from nicegui import ui
from sqlmodel import Session, select

from database import create_db_and_tables, engine
from models import Category, FoodItem


# สร้างไฟล์ SQLite และ tables หากยังไม่มี
create_db_and_tables()


# ============================================================
# Database functions
# ============================================================


def get_categories() -> list[Category]:
    """อ่าน Category ทั้งหมดจาก database"""
    with Session(engine) as session:
        statement = select(Category).order_by(Category.name)
        return list(session.exec(statement).all())


def get_food_items_by_category(category_id: int) -> list[FoodItem]:
    """อ่าน FoodItem ของ category ที่ระบุ"""
    with Session(engine) as session:
        statement = (
            select(FoodItem)
            .where(FoodItem.category_id == category_id)
            .order_by(FoodItem.name)
        )
        return list(session.exec(statement).all())


def get_category_options() -> dict[int, str]:
    """
    แปลง Category เป็นรูปแบบสำหรับ ui.select

    ตัวอย่าง:
    {1: "อาหารจานเดียว", 2: "เครื่องดื่ม"}
    """
    return {
        category.id: category.name
        for category in get_categories()
        if category.id is not None
    }


# ============================================================
# ส่วนแสดงเมนู
# ============================================================


@ui.refreshable
def show_menu_by_category() -> None:
    """แสดงรายการอาหารโดยจัดกลุ่มตาม Category"""
    categories = get_categories()

    if not categories:
        ui.label("ยังไม่มีหมวดหมู่หรือรายการอาหาร").classes("text-grey")
        return

    for category in categories:
        # ข้อมูลที่อ่านจาก database ควรมี id
        # แต่เช็กไว้เพื่อให้ type checker และโปรแกรมปลอดภัย
        if category.id is None:
            continue

        with ui.card().classes("w-full"):
            ui.label(category.name).classes("text-h6")

            food_items = get_food_items_by_category(category.id)

            if not food_items:
                ui.label("ยังไม่มีรายการอาหารในหมวดนี้").classes("text-grey")
                continue

            for food in food_items:
                with ui.row().classes("w-full justify-between"):
                    ui.label(food.name)
                    ui.label(f"{food.price:.2f} บาท").classes("font-bold")


# ============================================================
# User Interface
# ============================================================

ui.label("Food Order App").classes("text-h4")
ui.label("ตัวอย่าง NiceGUI + SQLModel + SQLite").classes("text-grey")


# ---------------- เพิ่ม Category ----------------
with ui.card().classes("w-full"):
    ui.label("เพิ่มหมวดหมู่อาหาร").classes("text-h6")

    category_name_input = ui.input(
        label="ชื่อหมวดหมู่",
        placeholder="เช่น อาหารจานเดียว",
    )

    def add_category() -> None:
        """เพิ่ม Category ใหม่ลง SQLite"""
        name = (category_name_input.value or "").strip()

        if not name:
            ui.notify("กรุณากรอกชื่อหมวดหมู่", type="warning")
            return

        with Session(engine) as session:
            session.add(Category(name=name))
            session.commit()

        # ล้างช่องกรอกข้อมูล
        category_name_input.value = ""
        category_name_input.update()

        # อัปเดตตัวเลือก Category ใน form เพิ่มอาหาร
        food_category_select.options = get_category_options()
        food_category_select.update()

        # วาดรายการเมนูใหม่
        show_menu_by_category.refresh()

        ui.notify(f'เพิ่มหมวดหมู่ "{name}" แล้ว', type="positive")

    ui.button("เพิ่มหมวดหมู่", on_click=add_category)


# ---------------- เพิ่ม Food Item ----------------
with ui.card().classes("w-full"):
    ui.label("เพิ่มรายการอาหาร").classes("text-h6")

    food_name_input = ui.input(
        label="ชื่ออาหาร",
        placeholder="เช่น ข้าวกะเพราหมูสับ",
    )

    food_price_input = ui.number(
        label="ราคา (บาท)",
        min=0,
        format="%.2f",
    )

    food_category_select = ui.select(
        options=get_category_options(),
        label="เลือกหมวดหมู่",
    )

    def add_food_item() -> None:
        """เพิ่ม FoodItem ใหม่ลง SQLite"""
        name = (food_name_input.value or "").strip()
        price = food_price_input.value
        category_id = food_category_select.value

        if not name:
            ui.notify("กรุณากรอกชื่ออาหาร", type="warning")
            return

        if price is None:
            ui.notify("กรุณากรอกราคา", type="warning")
            return

        if category_id is None:
            ui.notify("กรุณาเลือกหมวดหมู่", type="warning")
            return

        with Session(engine) as session:
            new_food = FoodItem(
                name=name,
                price=Decimal(price),
                category_id=int(category_id),
            )
            session.add(new_food)
            session.commit()

        # ล้าง form
        food_name_input.value = ""
        food_name_input.update()

        food_price_input.value = None
        food_price_input.update()

        # อัปเดตรายการเมนู
        show_menu_by_category.refresh()

        ui.notify(f'เพิ่มเมนู "{name}" แล้ว', type="positive")

    ui.button("เพิ่มรายการอาหาร", on_click=add_food_item)


# ---------------- แสดงเมนู ----------------
ui.separator()
ui.label("เมนูอาหารแยกตามหมวดหมู่").classes("text-h5")
show_menu_by_category()


# ต้องไม่ใส่ main guard ในกรณีนี้
# เพราะ NiceGUI มีการ run script สำหรับสร้างหน้าให้ browser
ui.run(title="foodmenu/app.py")
