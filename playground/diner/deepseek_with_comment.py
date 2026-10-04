"""
โปรแกรมนี้ — NiceGUI Web App แสดง Category และ Menu
รัน: python <ซื่อโปรแกรม>
เปิดเบราว์เซอร์: http://localhost:8081  ดูผลลัพธ์

"""

# 👇 ปิด warning ของ Pylance/Mypy ที่เป็น false positive
#    เกิดจาก NiceGUI Table ใช้ชื่อ "Column" ชนกับ SQLModel Column
# pyright: reportAttributeAccessIssue=false
# mypy: disable-error-code="attr-defined"

# ----- Standard Library -----
from contextlib import contextmanager  # ใช้สร้าง Context Manager (with ...)
from decimal import Decimal  # ใช้เก็บราคาแบบทศนิยม (แม่นยำกว่า float)
from typing import Any, Iterator, Optional, cast
#  Any = อะไรก็ได้, Iterator = ตัววนซ้ำ, Optional = มีหรือไม่มีก็ได้
#  cast = บอก Type ให้ Type Checker เข้าใจ

# ----- Third-party -----
from nicegui import ui
#  ui = โมดูลหลักของ NiceGUI ใช้สร้าง UI ทั้งหมด
#  เช่น ui.label(), ui.table(), ui.row(), ui.page()

from sqlmodel import Session, SQLModel, col, select
#  Session = ตัวจัดการ transaction กับ DB
#  SQLModel = Base class ของทุก Model (ใน model.py)
#  col = helper ที่บอก Type Checker ว่า attribute นี้เป็น Column
#  select = สร้าง SQL SELECT statement

# ----- Local -----
from database import create_db_and_tables, engine
#  create_db_and_tables() = สร้างตารางถ้ายังไม่มี
#  engine = ตัวเชื่อมต่อกับไฟล์ food_order.db

from model import Category, Menu, MenuOption, MenuOptionLink, OptionGroup
#  โมเดลทั้งหมดที่เราจะใช้ query


# =========================================================
# Type Helper
# =========================================================
# 💡 ปัญหาที่เราเจอ: Pylance บอกว่า obj.id เป็น int | None
#    แต่จริงๆ หลัง flush() แล้วมันมีค่าแน่ๆ
#    เราเลยสร้าง helper นี้เพื่อ cast ให้เป็น int


def require_id(obj: SQLModel) -> int:
    """ดึง id จาก obj ที่ผ่าน flush() แล้ว (มีค่าแน่นอน)"""
    obj_id = getattr(obj, "id", None)
    #  getattr = ดึง attribute แบบปลอดภัย (ถ้าไม่มีจะได้ None)
    if obj_id is None:
        #  ถ้า id ยังเป็น None แสดงว่าลืม flush() → throw error ทันที
        raise RuntimeError(f"{type(obj).__name__} ยังไม่มี id — ลืม flush หรือเปล่า?")
    return cast(int, obj_id)
    #  cast(int, ...) = บอก Type Checker ว่า "เชื่อผม มันเป็น int"


# =========================================================
# Session Helper
# =========================================================
# 💡 Pattern นี้เรียกว่า "Context Manager"
#    ใช้ `with session_scope() as s:` แล้ว session จะเปิด-ปิดอัตโนมัติ
#    ถ้า error → rollback
#    ถ้าสำเร็จ → commit
#    ไม่ว่าเกิดอะไร → close() เสมอ


@contextmanager
def session_scope() -> Iterator[Session]:
    session = Session(engine)  # เปิด session ใหม่
    try:
        yield session  # 👈 ส่ง session ให้โค้ดที่เรียกใช้
        session.commit()  # ถ้าไม่มี error → commit
    except Exception:
        session.rollback()  # ถ้ามี error → ยกเลิกการเปลี่ยนแปลง
        raise  # แล้วโยน error ต่อ (ให้เราเห็น)
    finally:
        session.close()  # ⭐ สำคัญ: ปิด session ทุกกรณี


# =========================================================
# Data Access Functions
# =========================================================
# 💡 หลักการสำคัญ: "ห้ามคืน ORM object ออกนอก session"
#    เพราะหลัง session ปิด attribute จะถูก expire (ใช้ไม่ได้)
#    → เราจะแปลงเป็น dict ก่อนคืน


def fetch_categories() -> list[dict[str, Any]]:
    """ดึงหมวดหมู่ทั้งหมด"""
    with session_scope() as s:
        #  select(Category) = SELECT * FROM categories
        #  .order_by(col(Category.id)) = ORDER BY id
        #  col() ช่วยให้ Type Checker รู้ว่านี่คือ Column
        rows = s.exec(select(Category).order_by(col(Category.id))).all()

        #  👇 แปลง ORM → dict ทันที "ภายใน" session
        #    เพื่อไม่ให้เจอ DetachedInstanceError ทีหลัง
        return [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
                "is_active": c.is_active,
                "created_at": c.created_at,
            }
            for c in rows
        ]


def fetch_menus(category_id: Optional[int] = None) -> list[dict[str, Any]]:
    """ดึงเมนูทั้งหมด (หรือเฉพาะ category_id ที่ระบุ)"""
    with session_scope() as s:
        stmt = select(Menu).order_by(col(Menu.id))

        #  👇 ถ้ามีการกรอง category → เพิ่ม WHERE เข้าไป
        if category_id is not None:
            stmt = stmt.where(col(Menu.category_id) == category_id)

        rows = s.exec(stmt).all()
        return [
            {
                "id": m.id,
                "category_id": m.category_id,
                "name": m.name,
                "description": m.description,
                "base_price": m.base_price,
                "is_active": m.is_active,
            }
            for m in rows
        ]


def fetch_category_map() -> dict[int, str]:
    """คืน {id: name} ไว้ใช้แปลง category_id → ชื่อหมวดหมู่"""
    with session_scope() as s:
        rows = s.exec(select(Category)).all()
        #  👇 Dictionary comprehension + เช็ค id ไม่ใช่ None
        return {int(c.id): c.name for c in rows if c.id is not None}


def fetch_menu_options(menu_id: int) -> list[tuple[str, str, Decimal]]:
    """
    ดึงตัวเลือก (options) ของเมนูที่ระบุ
    คืน list ของ (ชื่อกลุ่ม, ชื่อ option, ราคาเพิ่ม)
    """
    with session_scope() as s:
        #  ⚠️ กับดักที่เราเจอ:
        #    .join(col(A) == col(B))   ❌ ผิด (ส่ง condition ไป)
        #    .join(B, col(A) == col(B)) ✅ ถูก (ส่งตาราง + condition)
        stmt = (
            select(OptionGroup, MenuOption)  # 👈 select ตารางเต็ม (2 ตาราง)
            .join(
                MenuOption,
                col(MenuOption.option_group_id) == col(OptionGroup.id),
                #  👆 join ตาราง MenuOption ด้วย condition นี้
            )
            .join(
                MenuOptionLink,
                col(MenuOptionLink.menu_option_id) == col(MenuOption.id),
            )
            .where(col(MenuOptionLink.menu_id) == menu_id)
        )
        rows = s.exec(stmt).all()

        #  👇 rows = [(OptionGroup, MenuOption), ...]
        #    แตก tuple แล้วเข้าถึง attribute ปกติ
        return [
            (str(g.name), str(o.name), Decimal(str(o.extra_price))) for g, o in rows
        ]


def fetch_stats() -> dict[str, int]:
    """นับจำนวนสำหรับแสดง Stats Cards"""
    with session_scope() as s:
        return {
            "categories": len(s.exec(select(Category)).all()),
            "menus": len(s.exec(select(Menu)).all()),
            #  👇 .is_(True) แทน == True (หลบ Linter บ่น)
            "active_menus": len(
                s.exec(select(Menu).where(col(Menu.is_active).is_(True))).all()
            ),
        }


# =========================================================
# Seed Data — ใส่ข้อมูลตัวอย่างถ้าฐานข้อมูลว่าง
# =========================================================


def seed_if_empty() -> None:
    with session_scope() as s:
        #  👇 ถ้ามี Category อยู่แล้ว → ข้าม (ไม่ใส่ซ้ำ)
        if s.exec(select(Category)).first() is not None:
            return

        # --- 1. สร้าง Categories ---
        cat_food = Category(name="อาหารจานหลัก", description="ข้าว ผัด ก๋วยเตี๋ยว")
        cat_drink = Category(name="เครื่องดื่ม", description="น้ำผลไม้ ชา กาแฟ")
        cat_dessert = Category(name="ของหวาน", description="ไอศครีม ขนมไทย")
        s.add_all([cat_food, cat_drink, cat_dessert])

        #  ⭐ flush() = ส่ง SQL INSERT ไป DB แต่ยังไม่ commit
        #    ทำให้ได้ id กลับมา (auto-increment)
        s.flush()

        # --- 2. สร้าง OptionGroups ---
        g_spicy = OptionGroup(
            name="ระดับความเผ็ด", allow_multiple=False, is_required=True
        )
        g_size = OptionGroup(name="ขนาด", allow_multiple=False, is_required=False)
        g_topping = OptionGroup(name="ท็อปปิ้ง", allow_multiple=True, is_required=False)
        s.add_all([g_spicy, g_size, g_topping])
        s.flush()

        #  👇 ใช้ require_id() เพื่อให้ได้ int (ไม่ใช่ int | None)
        spicy_id = require_id(g_spicy)
        size_id = require_id(g_size)
        topping_id = require_id(g_topping)

        # --- 3. สร้าง MenuOptions ---
        o_mild = MenuOption(
            option_group_id=spicy_id, name="ไม่เผ็ด", extra_price=Decimal("0.00")
        )
        o_medium = MenuOption(
            option_group_id=spicy_id, name="เผ็ดกลาง", extra_price=Decimal("0.00")
        )
        o_hot = MenuOption(
            option_group_id=spicy_id, name="เผ็ดมาก", extra_price=Decimal("5.00")
        )
        o_s = MenuOption(
            option_group_id=size_id, name="เล็ก", extra_price=Decimal("0.00")
        )
        o_m = MenuOption(
            option_group_id=size_id, name="กลาง", extra_price=Decimal("10.00")
        )
        o_l = MenuOption(
            option_group_id=size_id, name="ใหญ่", extra_price=Decimal("20.00")
        )
        o_egg = MenuOption(
            option_group_id=topping_id, name="ไข่ดาว", extra_price=Decimal("10.00")
        )
        o_cheese = MenuOption(
            option_group_id=topping_id, name="ชีส", extra_price=Decimal("15.00")
        )
        s.add_all([o_mild, o_medium, o_hot, o_s, o_m, o_l, o_egg, o_cheese])
        s.flush()

        # --- 4. สร้าง Menus ---
        food_id = require_id(cat_food)
        drink_id = require_id(cat_drink)
        dessert_id = require_id(cat_dessert)

        m1 = Menu(
            category_id=food_id,
            name="ผัดไทยกุ้งสด",
            description="ผัดไทยสูตรโบราณ เส้นเหนียวนุ่ม",
            base_price=Decimal("80.00"),
        )
        m2 = Menu(
            category_id=food_id,
            name="ข้าวผัดกระเพราหมูสับ",
            description="กระเพราแท้ หอมใบกระเพรา",
            base_price=Decimal("65.00"),
        )
        m3 = Menu(
            category_id=food_id,
            name="ต้มยำกุ้งน้ำข้น",
            description="ต้มยำรสจัดจ้าน",
            base_price=Decimal("120.00"),
        )
        m4 = Menu(
            category_id=drink_id,
            name="ชาไทยเย็น",
            description="ชาไทยสูตรเข้มข้น",
            base_price=Decimal("45.00"),
        )
        m5 = Menu(
            category_id=drink_id,
            name="น้ำส้มคั้นสด",
            description="ส้มคั้นสด 100%",
            base_price=Decimal("55.00"),
        )
        m6 = Menu(
            category_id=dessert_id,
            name="ไอศครีมกะทิ",
            description="ไอศครีมกะทิสด เสิร์ฟพร้อมถั่วลิสง",
            base_price=Decimal("50.00"),
        )
        s.add_all([m1, m2, m3, m4, m5, m6])
        s.flush()

        # --- 5. เชื่อม Menu ↔ MenuOption ---
        links = [
            MenuOptionLink(menu_id=require_id(m1), menu_option_id=require_id(o_hot)),
            MenuOptionLink(menu_id=require_id(m1), menu_option_id=require_id(o_egg)),
            MenuOptionLink(menu_id=require_id(m2), menu_option_id=require_id(o_mild)),
            MenuOptionLink(menu_id=require_id(m2), menu_option_id=require_id(o_medium)),
            MenuOptionLink(menu_id=require_id(m2), menu_option_id=require_id(o_hot)),
            MenuOptionLink(menu_id=require_id(m2), menu_option_id=require_id(o_egg)),
            MenuOptionLink(menu_id=require_id(m3), menu_option_id=require_id(o_hot)),
            MenuOptionLink(menu_id=require_id(m4), menu_option_id=require_id(o_s)),
            MenuOptionLink(menu_id=require_id(m4), menu_option_id=require_id(o_m)),
            MenuOptionLink(menu_id=require_id(m5), menu_option_id=require_id(o_m)),
            MenuOptionLink(menu_id=require_id(m6), menu_option_id=require_id(o_cheese)),
        ]
        s.add_all(links)
        #  👇 ออกจาก with → session.commit() ถูกเรียกอัตโนมัติ


# =========================================================
# UI Components
# =========================================================


def render_stats() -> None:
    """แสดง 3 การ์ดสรุปด้านบน"""
    stats = fetch_stats()
    #  👇 ui.row() = จัดเรียงแนวนอน, .classes() = ใส่ Tailwind CSS
    with ui.row().classes("w-full gap-4 mb-4"):
        for label, key, color in [
            ("หมวดหมู่ทั้งหมด", "categories", "blue"),
            ("เมนูทั้งหมด", "menus", "green"),
            ("เมนูที่เปิดขาย", "active_menus", "orange"),
        ]:
            #  👇 ui.card() = การ์ด
            with ui.card().classes(f"flex-1 bg-{color}-1 border border-{color}-3"):
                ui.label(label).classes("text-sm text-gray-600")
                ui.label(str(stats[key])).classes(f"text-3xl font-bold text-{color}-8")


def render_category_table() -> None:
    """แสดงตารางหมวดหมู่"""
    categories = fetch_categories()

    #  👇 columns = คำอธิบายคอลัมน์ของตาราง
    #    แต่ละตัวเป็น dict ที่มี name/label/field/align
    columns = [
        {"name": "id", "label": "ID", "field": "id", "align": "left"},
        {"name": "name", "label": "ชื่อหมวดหมู่", "field": "name", "align": "left"},
        {
            "name": "description",
            "label": "คำอธิบาย",
            "field": "description",
            "align": "left",
        },
        {
            "name": "is_active",
            "label": "เปิดใช้งาน",
            "field": "is_active",
            "align": "center",
        },
        {
            "name": "created_at",
            "label": "สร้างเมื่อ",
            "field": "created_at",
            "align": "left",
        },
    ]

    #  👇 แปลงข้อมูลเป็น row (dict ที่ตรงกับ field ใน columns)
    rows = [
        {
            "id": c["id"],
            "name": c["name"],
            "description": c["description"] or "-",  # ถ้า None → "-"
            "is_active": "✅" if c["is_active"] else "❌",
            "created_at": c["created_at"].strftime("%Y-%m-%d %H:%M"),
        }
        for c in categories
    ]
    ui.table(columns=columns, rows=rows, row_key="id").classes("w-full")


def render_menu_table(category_filter: Optional[int] = None) -> None:
    """แสดงตารางเมนู (กรองตาม category_filter ได้)"""
    menus = fetch_menus(category_filter)
    cat_map = fetch_category_map()  # {id: name} ไว้แปลง category_id
    columns = [
        {"name": "id", "label": "ID", "field": "id", "align": "left"},
        {"name": "name", "label": "ชื่อเมนู", "field": "name", "align": "left"},
        {"name": "category", "label": "หมวดหมู่", "field": "category", "align": "left"},
        {
            "name": "description",
            "label": "คำอธิบาย",
            "field": "description",
            "align": "left",
        },
        {
            "name": "base_price",
            "label": "ราคา (บาท)",
            "field": "base_price",
            "align": "right",
        },
        {
            "name": "is_active",
            "label": "เปิดขาย",
            "field": "is_active",
            "align": "center",
        },
    ]
    rows = [
        {
            "id": m["id"],
            "name": m["name"],
            #  👇 ใช้ .get() ปลอดภัยกว่า [] (ไม่ throw ถ้าไม่มี key)
            "category": cat_map.get(m["category_id"], f"#{m['category_id']}"),
            "description": m["description"] or "-",
            "base_price": f"{m['base_price']:,.2f}",  # 1,234.50
            "is_active": "✅" if m["is_active"] else "❌",
        }
        for m in menus
    ]
    ui.table(columns=columns, rows=rows, row_key="id").classes("w-full")


def render_menu_detail_dialog() -> Any:
    """สร้าง Dialog แสดงรายละเอียดเมนู"""
    menus = fetch_menus()
    cat_map = fetch_category_map()

    #  👇 dict สำหรับใส่ใน ui.select: {id: name}
    menu_options: dict[int, str] = {
        int(m["id"]): m["name"] for m in menus if m["id"] is not None
    }

    #  👇 ui.dialog() = หน้าต่าง popup
    #    ui.card() = การ์ดข้างใน
    with ui.dialog() as dialog, ui.card().classes("w-[600px] max-w-full"):
        ui.label("รายละเอียดเมนูและตัวเลือก").classes("text-lg font-bold mb-2")
        detail_container = ui.column().classes("w-full gap-2")
        #  👆 container เปล่าๆ ไว้ใส่เนื้อหาทีหลัง (ตอนเลือกเมนู)

        def show_detail(menu_id: int) -> None:
            """แสดงรายละเอียดของเมนูที่เลือก"""
            detail_container.clear()  # ล้างของเก่า
            menu = next((m for m in menus if m["id"] == menu_id), None)
            if menu is None:
                with detail_container:
                    ui.label("ไม่พบเมนู")
                return
            with detail_container:
                ui.label(f"🍽️ {menu['name']}").classes("text-xl font-bold")
                ui.label(f"หมวดหมู่: {cat_map.get(menu['category_id'], '-')}")
                ui.label(f"คำอธิบาย: {menu['description'] or '-'}")
                ui.label(f"ราคา: {menu['base_price']:,.2f} บาท")
                ui.separator()
                ui.label("ตัวเลือกที่มี:").classes("font-bold")

                #  👇 ดึง options ผ่านฟังก์ชันที่แก้ join แล้ว
                opts = fetch_menu_options(menu_id)
                if not opts:
                    ui.label("(ไม่มีตัวเลือก)").classes("text-gray-500 italic")
                else:
                    for group_name, opt_name, extra in opts:
                        price_txt = f"+{extra:,.2f}" if extra > 0 else "ฟรี"
                        ui.label(f"• [{group_name}] {opt_name} ({price_txt})")

        def on_select(e: Any) -> None:
            """callback เมื่อผู้ใช้เลือกเมนูจาก dropdown"""
            if e.value is not None:
                show_detail(int(e.value))

        ui.select(
            options=menu_options,
            label="เลือกเมนู",
            on_change=on_select,
        ).classes("w-full")

        #  👇 เลือกเมนูแรกอัตโนมัติ (ให้ผู้ใช้เห็นทันทีไม่ต้องคลิก)
        if menu_options:
            first_id = next(iter(menu_options))  # ดึง key แรก
            show_detail(first_id)

        with ui.row().classes("w-full justify-end mt-4"):
            ui.button("ปิด", on_click=dialog.close).props("flat")

    return dialog  # ⭐ ต้อง return เพื่อให้ main_page() เอาไปใช้ .open()


# =========================================================
# Page Layout
# =========================================================
# 💡 @ui.page("/") = กำหนดว่าฟังก์ชันนี้คือหน้าเว็บที่ path "/"
#    ทุกครั้งที่ user เข้า "/" ฟังก์ชันจะถูกเรียกใหม่
#    ทำให้ข้อมูล refresh ทุกครั้ง


@ui.page("/")
def main_page() -> None:
    ui.colors(primary="#2563eb")
    #  👆 ตั้งสี primary (ใช้กับ .props("color=primary"))

    ui.query("body").style("background-color: #f5f7fa")
    #  👆 ใส่ CSS ให้ <body> โดยตรง

    # --- Header (แถบด้านบน) ---
    with ui.header().classes(
        "items-center justify-between bg-primary text-white px-6 py-3"
    ):
        with ui.row().classes("items-center gap-3"):
            ui.icon("restaurant_menu", size="32px")  # ไอคอน Material
            ui.label("ระบบจัดการเมนูอาหาร").classes("text-xl font-bold")
        ui.label("Demo: NiceGUI + SQLModel").classes("text-sm opacity-80")

    # --- Main Content ---
    with ui.column().classes("w-full max-w-7xl mx-auto p-6 gap-6"):
        #  👆 column = จัดเรียงแนวตั้ง, max-w-7xl = จำกัดความกว้าง, mx-auto = จัดกลาง

        render_stats()

        # --- Section: Categories ---
        with ui.card().classes("w-full"):
            with ui.row().classes("items-center justify-between w-full mb-2"):
                with ui.row().classes("items-center gap-2"):
                    ui.icon("category", size="24px").classes("text-blue-600")
                    ui.label("หมวดหมู่ (Categories)").classes("text-lg font-bold")
                #  👇 ปุ่ม refresh → navigate ไป "/" (โหลดใหม่)
                ui.button(
                    icon="refresh",
                    on_click=lambda: ui.navigate.to("/"),
                ).props("flat round")
            render_category_table()

        # --- Section: Menus ---
        with ui.card().classes("w-full"):
            with ui.row().classes("items-center justify-between w-full mb-2"):
                with ui.row().classes("items-center gap-2"):
                    ui.icon("menu_book", size="24px").classes("text-green-600")
                    ui.label("เมนูอาหาร (Menus)").classes("text-lg font-bold")

                #  👇 เตรียม dropdown กรองหมวดหมู่
                cats = fetch_categories()
                filter_options: dict[str, Optional[int]] = {"ทั้งหมด": None}
                for c in cats:
                    filter_options[str(c["name"])] = c["id"]

                #  👇 container เปล่า ไว้ใส่ตารางทีหลัง (ตอนกรอง)
                menu_table_container = ui.column().classes("w-full")
                selected_filter: dict[str, Optional[int]] = {"value": None}
                #  👆 ใช้ dict เก็บค่า เพราะ Python closure ต้อง mutate ได้

                def rebuild_menu_table() -> None:
                    """สร้างตารางใหม่ตาม filter ปัจจุบัน"""
                    menu_table_container.clear()
                    with menu_table_container:
                        render_menu_table(category_filter=selected_filter["value"])

                def on_filter_change(e: Any) -> None:
                    """callback เมื่อเปลี่ยน dropdown"""
                    selected_filter["value"] = e.value
                    rebuild_menu_table()

                ui.select(
                    options=filter_options,
                    value=None,
                    label="กรองตามหมวดหมู่",
                    on_change=on_filter_change,
                ).classes("w-56")

            #  👇 เรียกครั้งแรกเพื่อแสดงตาราง
            rebuild_menu_table()

        # --- Section: Detail Dialog ---
        #  ⚠️ ต้องสร้าง dialog ก่อน แล้วเอา .open ไปผูกกับปุ่ม
        detail_dialog = render_menu_detail_dialog()

        with ui.card().classes("w-full"):
            with ui.row().classes("items-center gap-2"):
                ui.icon("info", size="24px").classes("text-purple-600")
                ui.label("ดูรายละเอียดเมนูและตัวเลือก").classes("text-lg font-bold")
            ui.button(
                "เปิดดูรายละเอียดเมนู",
                icon="visibility",
                on_click=detail_dialog.open,  # 👈 ผูก event
            ).props("color=purple")

    # --- Footer (แถบล่าง) ---
    with ui.footer().classes("bg-gray-100 text-gray-600 text-xs justify-center"):
        ui.label("© 2024 Food Order Demo — NiceGUI + SQLModel")


# # =========================================================
# # Entry Point
# # =========================================================
# # 💡 `__name__` จะเป็น "__main__" เมื่อรันตรงๆ
# #    และเป็น "__mp_main__" เมื่อ NiceGUI ใช้ multiprocessing
# #    (NiceGUI มี reload mode ที่ spawn process ใหม่)

# if __name__ in {"__main__", "__mp_main__"}:
#     create_db_and_tables()  # 1. สร้างตารางถ้ายังไม่มี
#     seed_if_empty()  # 2. ใส่ข้อมูลตัวอย่างถ้าว่าง
#     ui.run(  # 3. เริ่มเว็บเซิร์ฟเวอร์
#         title="Food Order Demo",
#         favicon="🍽️",
#         reload=False,  # 👈 ปิด reload (ไม่งั้น port ซ้ำ)
#         port=8081,  # 👈 เลี่ยง 8080 ที่มักถูก占用
#         show=True,  # เปิดเบราว์เซอร์อัตโนมัติ
#     )
# =========================================================
# Entry Point
# =========================================================
# 💡 `__name__` จะเป็น "__main__" เมื่อรันตรงๆ
#    และเป็น "__mp_main__" เมื่อ NiceGUI ใช้ multiprocessing

if __name__ in {"__main__", "__mp_main__"}:
    create_db_and_tables()  # 1. สร้างตารางถ้ายังไม่มี
    seed_if_empty()  # 2. ใส่ข้อมูลตัวอย่างถ้าว่าง

    # 👇 ครอบ ui.run() ด้วย try/except เพื่อจับ CTRL+C
    try:
        ui.run(  # 3. เริ่มเว็บเซิร์ฟเวอร์
            title="Food Order Demo",
            favicon="🍽️",
            reload=False,  # ปิด reload (ไม่งั้น port ซ้ำ)
            port=8081,  # เลี่ยง 8080 ที่มักถูก占用
            show=True,  # เปิดเบราว์เซอร์อัตโนมัติ
        )

    # 🎯 จับ KeyboardInterrupt = ผู้ใช้กด CTRL+C
    except KeyboardInterrupt:
        # พิมพ์ข้อความสวยๆ แทน traceback ยาวๆ
        print("\n👋 ปิดเซิร์ฟเวอร์เรียบร้อย — ขอบคุณที่ใช้งานครับ!")

    # 🎯 จับ CancelledError ที่อาจหลุดออกมาจาก asyncio
    #    (ในบาง Python version จะไม่ถูกจับโดย KeyboardInterrupt ตรงๆ)
    except BaseException as e:
        # ตรวจสอบว่าเป็น CancelledError หรือ KeyboardInterrupt
        # ที่ห่ออยู่ใน ExceptionGroup หรือไม่
        if "CancelledError" in str(type(e).__name__) or isinstance(
            e, KeyboardInterrupt
        ):
            print("\n👋 ปิดเซิร์ฟเวอร์เรียบร้อย — ขอบคุณที่ใช้งานครับ!")
        else:
            # ถ้าเป็น error อื่นจริงๆ → ให้แสดงตามปกติ
            raise
