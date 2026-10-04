from decimal import Decimal
from typing import Optional
from icecream import ic
from nicegui import ui
from sqlmodel import Session, select

# Import engine และ Model จากไฟล์ที่คุณกำหนดไว้
from database import create_db_and_tables, engine
from model import Category, Menu

ic("*" * 20)


def get_active_categories() -> list[Category]:
    """ดึงรายชื่อ Category ทั้งหมดที่ active อยู่ใน DB"""
    with Session(engine) as session:
        statement = select(Category).where(Category.is_active)
        categories: list[Category] = list(session.exec(statement).all())
        return categories


def save_category(name_input: ui.input, desc_input: ui.input) -> None:
    """Logic สำหรับบันทึกหมวดหมู่ใหม่ลงใน DB"""
    raw_name: Optional[str] = name_input.value
    raw_desc: Optional[str] = desc_input.value

    if not raw_name or not raw_name.strip():
        ui.notify("กรุณากรอกชื่อหมวดหมู่!", type="warning")
        return

    category_name: str = raw_name.strip()
    category_desc: Optional[str] = raw_desc.strip() if raw_desc else None

    new_category: Category = Category(
        name=category_name,
        description=category_desc,
    )

    try:
        with Session(engine) as session:
            session.add(new_category)
            session.commit()
            session.refresh(new_category)

        ui.notify(
            f"บันทึกหมวดหมู่ '{new_category.name}' เรียบร้อยแล้ว!",
            type="positive",
        )

        name_input.value = ""
        desc_input.value = ""
        ui.navigate.reload()

    except Exception as err:
        ui.notify(f"เกิดข้อผิดพลาด: {err}", type="negative")


def save_menu(
    category_select: ui.select,
    name_input: ui.input,
    price_input: ui.number,
    desc_input: ui.input,
) -> None:
    """Logic สำหรับบันทึกเมนูใหม่ลงใน DB"""
    ic()
    selected_category_id: Optional[int] = category_select.value
    raw_name: Optional[str] = name_input.value
    raw_price: Optional[float] = price_input.value
    raw_desc: Optional[str] = desc_input.value

    if not selected_category_id:
        ui.notify("กรุณาเลือกหมวดหมู่!", type="warning")
        return

    if not raw_name or not raw_name.strip():
        ui.notify("กรุณากรอกชื่อเมนู!", type="warning")
        return

    if raw_price is None or raw_price < 0:
        ui.notify("กรุณากรอกราคาที่ถูกต้อง!", type="warning")
        return

    menu_name: str = raw_name.strip()
    menu_desc: Optional[str] = raw_desc.strip() if raw_desc else None
    base_price: Decimal = Decimal(str(raw_price))

    new_menu: Menu = Menu(
        category_id=selected_category_id,
        name=menu_name,
        base_price=base_price,
        description=menu_desc,
    )
    ic("Data to save to menu: ")
    ic(new_menu)

    try:
        with Session(engine) as session:
            session.add(new_menu)
            session.commit()
            # แก้ไข: เพิ่ม session.refresh(new_menu) ก่อนปิด Session
            # เพื่อโหลดข้อมูล attribute ล่าสุดกลับเข้า instance
            session.refresh(new_menu)

        # เข้าถึง new_menu.name ได้อย่างปลอดภัย
        ui.notify(f"บันทึกเมนู '{new_menu.name}' เรียบร้อยแล้ว!", type="positive")

        name_input.value = ""
        price_input.value = None
        desc_input.value = ""

    except Exception as err:
        ui.notify(f"เกิดข้อผิดพลาดในการบันทึก: {err}", type="negative")


# =========================================================
# UI Layout (NiceGUI Elements)
# =========================================================


def build_gui() -> None:
    """ฟังก์ชันหลักสำหรับจัดวาง Elements บนหน้า Web App"""
    ui.label("ระบบจัดการเมนูอาหาร (Food Order App)").classes("text-2xl font-bold mb-4")
    ic("def build_gui()")
    ic()
    # --- ส่วนที่ 1: ฟอร์มเพิ่ม Category ---
    with ui.card().classes("w-full max-w-md mb-6"):
        ui.label("1. เพิ่มหมวดหมู่ (Category)").classes("text-lg font-semibold")

        cat_name_input = ui.input(
            label="ชื่อหมวดหมู่ *", placeholder="เช่น อาหารจานเดียว, เครื่องดื่ม"
        )
        cat_desc_input = ui.input(
            label="รายละเอียด", placeholder="คำอธิบายเพิ่มเติม (ไม่บังคับ)"
        )

        ui.button(
            "บันทึกหมวดหมู่",
            on_click=lambda: save_category(cat_name_input, cat_desc_input),
        )

    # --- ส่วนที่ 2: ฟอร์มเพิ่ม Menu ---
    with ui.card().classes("w-full max-w-md"):
        ui.label("2. เพิ่มเมนูอาหาร (Menu)").classes("text-lg font-semibold")

        categories: list[Category] = get_active_categories()
        category_options: dict[int, str] = {
            cat.id: cat.name for cat in categories if cat.id is not None
        }

        cat_select = ui.select(
            options=category_options,
            label="เลือกหมวดหมู่ *",
            with_input=True,
        )

        menu_name_input = ui.input(
            label="ชื่อเมนู *", placeholder="เช่น ข้าวกะเพราไก่, ชาไทย"
        )
        menu_price_input = ui.number(
            label="ราคา (บาท) *", precision=2, placeholder="0.00"
        )
        menu_desc_input = ui.input(
            label="รายละเอียดเมนู", placeholder="คำอธิบายเพิ่มเติม (ไม่บังคับ)"
        )

        ui.button(
            "บันทึกเมนู",
            on_click=lambda: save_menu(
                cat_select,
                menu_name_input,
                menu_price_input,
                menu_desc_input,
            ),
        )


ic("Main UI before ui")

create_db_and_tables()
build_gui()

ui.run(title="add_menu_and_cat.py", port=8080)
