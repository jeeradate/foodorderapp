"""
app.py — NiceGUI Web App แสดง Category และ Menu
รัน: python app.py
เปิดเบราว์เซอร์: http://localhost:8081
"""

# pyright: reportAttributeAccessIssue=false
# mypy: disable-error-code="attr-defined"

from contextlib import contextmanager
from decimal import Decimal
from typing import Any, Iterator, Optional, cast

from nicegui import ui

# from sqlalchemy import and_  # 👈 เพิ่ม
from sqlmodel import Session, SQLModel, col, select

from database import create_db_and_tables, engine
from model import Category, Menu, MenuOption, MenuOptionLink, OptionGroup


# =========================================================
# Type Helper
# =========================================================


def require_id(obj: SQLModel) -> int:
    obj_id = getattr(obj, "id", None)
    if obj_id is None:
        raise RuntimeError(f"{type(obj).__name__} ยังไม่มี id — ลืม flush หรือเปล่า?")
    return cast(int, obj_id)


# =========================================================
# Session Helper
# =========================================================


@contextmanager
def session_scope() -> Iterator[Session]:
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# =========================================================
# Data Access Functions — คืนเป็น dict ทั้งหมด
# =========================================================


def fetch_categories() -> list[dict[str, Any]]:
    with session_scope() as s:
        rows = s.exec(select(Category).order_by(col(Category.id))).all()
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
    with session_scope() as s:
        stmt = select(Menu).order_by(col(Menu.id))
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
    with session_scope() as s:
        rows = s.exec(select(Category)).all()
        return {int(c.id): c.name for c in rows if c.id is not None}


def fetch_menu_options(menu_id: int) -> list[tuple[str, str, Decimal]]:
    """ดึง (group_name, option_name, extra_price) ของเมนูที่ระบุ"""
    with session_scope() as s:
        stmt = (
            select(OptionGroup, MenuOption)
            .join(
                MenuOption,
                col(MenuOption.option_group_id)
                == col(OptionGroup.id),  # 👈 ใช้ join(condition)
            )
            .join(
                MenuOptionLink,
                col(MenuOptionLink.menu_option_id) == col(MenuOption.id),
            )
            .where(col(MenuOptionLink.menu_id) == menu_id)
        )
        rows = s.exec(stmt).all()
        return [
            (str(g.name), str(o.name), Decimal(str(o.extra_price))) for g, o in rows
        ]


def fetch_stats() -> dict[str, int]:
    with session_scope() as s:
        return {
            "categories": len(s.exec(select(Category)).all()),
            "menus": len(s.exec(select(Menu)).all()),
            "active_menus": len(
                s.exec(select(Menu).where(col(Menu.is_active).is_(True))).all()
            ),
        }


# =========================================================
# Seed Data
# =========================================================


def seed_if_empty() -> None:
    with session_scope() as s:
        if s.exec(select(Category)).first() is not None:
            return

        cat_food = Category(name="อาหารจานหลัก", description="ข้าว ผัด ก๋วยเตี๋ยว")
        cat_drink = Category(name="เครื่องดื่ม", description="น้ำผลไม้ ชา กาแฟ")
        cat_dessert = Category(name="ของหวาน", description="ไอศครีม ขนมไทย")
        s.add_all([cat_food, cat_drink, cat_dessert])
        s.flush()

        g_spicy = OptionGroup(
            name="ระดับความเผ็ด", allow_multiple=False, is_required=True
        )
        g_size = OptionGroup(name="ขนาด", allow_multiple=False, is_required=False)
        g_topping = OptionGroup(name="ท็อปปิ้ง", allow_multiple=True, is_required=False)
        s.add_all([g_spicy, g_size, g_topping])
        s.flush()

        spicy_id = require_id(g_spicy)
        size_id = require_id(g_size)
        topping_id = require_id(g_topping)

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


# =========================================================
# UI Components
# =========================================================


def render_stats() -> None:
    stats = fetch_stats()
    with ui.row().classes("w-full gap-4 mb-4"):
        for label, key, color in [
            ("หมวดหมู่ทั้งหมด", "categories", "blue"),
            ("เมนูทั้งหมด", "menus", "green"),
            ("เมนูที่เปิดขาย", "active_menus", "orange"),
        ]:
            with ui.card().classes(f"flex-1 bg-{color}-1 border border-{color}-3"):
                ui.label(label).classes("text-sm text-gray-600")
                ui.label(str(stats[key])).classes(f"text-3xl font-bold text-{color}-8")


def render_category_table() -> None:
    categories = fetch_categories()
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
    rows = [
        {
            "id": c["id"],
            "name": c["name"],
            "description": c["description"] or "-",
            "is_active": "✅" if c["is_active"] else "❌",
            "created_at": c["created_at"].strftime("%Y-%m-%d %H:%M"),
        }
        for c in categories
    ]
    ui.table(columns=columns, rows=rows, row_key="id").classes("w-full")


def render_menu_table(category_filter: Optional[int] = None) -> None:
    menus = fetch_menus(category_filter)
    cat_map = fetch_category_map()
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
            "category": cat_map.get(m["category_id"], f"#{m['category_id']}"),
            "description": m["description"] or "-",
            "base_price": f"{m['base_price']:,.2f}",
            "is_active": "✅" if m["is_active"] else "❌",
        }
        for m in menus
    ]
    ui.table(columns=columns, rows=rows, row_key="id").classes("w-full")


def render_menu_detail_dialog() -> Any:
    menus = fetch_menus()
    cat_map = fetch_category_map()

    menu_options: dict[int, str] = {
        int(m["id"]): m["name"] for m in menus if m["id"] is not None
    }

    with ui.dialog() as dialog, ui.card().classes("w-[600px] max-w-full"):
        ui.label("รายละเอียดเมนูและตัวเลือก").classes("text-lg font-bold mb-2")
        detail_container = ui.column().classes("w-full gap-2")

        def show_detail(menu_id: int) -> None:
            detail_container.clear()
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
                opts = fetch_menu_options(menu_id)
                if not opts:
                    ui.label("(ไม่มีตัวเลือก)").classes("text-gray-500 italic")
                else:
                    for group_name, opt_name, extra in opts:
                        price_txt = f"+{extra:,.2f}" if extra > 0 else "ฟรี"
                        ui.label(f"• [{group_name}] {opt_name} ({price_txt})")

        def on_select(e: Any) -> None:
            if e.value is not None:
                show_detail(int(e.value))

        ui.select(options=menu_options, label="เลือกเมนู", on_change=on_select).classes(
            "w-full"
        )

        if menu_options:
            first_id = next(iter(menu_options))
            show_detail(first_id)

        with ui.row().classes("w-full justify-end mt-4"):
            ui.button("ปิด", on_click=dialog.close).props("flat")

    return dialog


# =========================================================
# Page Layout
# =========================================================


@ui.page("/")
def main_page() -> None:
    ui.colors(primary="#2563eb")
    ui.query("body").style("background-color: #f5f7fa")

    with ui.header().classes(
        "items-center justify-between bg-primary text-white px-6 py-3"
    ):
        with ui.row().classes("items-center gap-3"):
            ui.icon("restaurant_menu", size="32px")
            ui.label("ระบบจัดการเมนูอาหาร").classes("text-xl font-bold")
        ui.label("Demo: NiceGUI + SQLModel").classes("text-sm opacity-80")

    with ui.column().classes("w-full max-w-7xl mx-auto p-6 gap-6"):
        render_stats()

        with ui.card().classes("w-full"):
            with ui.row().classes("items-center justify-between w-full mb-2"):
                with ui.row().classes("items-center gap-2"):
                    ui.icon("category", size="24px").classes("text-blue-600")
                    ui.label("หมวดหมู่ (Categories)").classes("text-lg font-bold")
                ui.button(icon="refresh", on_click=lambda: ui.navigate.to("/")).props(
                    "flat round"
                )
            render_category_table()

        with ui.card().classes("w-full"):
            with ui.row().classes("items-center justify-between w-full mb-2"):
                with ui.row().classes("items-center gap-2"):
                    ui.icon("menu_book", size="24px").classes("text-green-600")
                    ui.label("เมนูอาหาร (Menus)").classes("text-lg font-bold")

                cats = fetch_categories()
                filter_options: dict[str, Optional[int]] = {"ทั้งหมด": None}
                for c in cats:
                    filter_options[str(c["name"])] = c["id"]

                menu_table_container = ui.column().classes("w-full")
                selected_filter: dict[str, Optional[int]] = {"value": None}

                def rebuild_menu_table() -> None:
                    menu_table_container.clear()
                    with menu_table_container:
                        render_menu_table(category_filter=selected_filter["value"])

                def on_filter_change(e: Any) -> None:
                    selected_filter["value"] = e.value
                    rebuild_menu_table()

                ui.select(
                    options=filter_options,
                    value=None,
                    label="กรองตามหมวดหมู่",
                    on_change=on_filter_change,
                ).classes("w-56")

            rebuild_menu_table()

        detail_dialog = render_menu_detail_dialog()

        with ui.card().classes("w-full"):
            with ui.row().classes("items-center gap-2"):
                ui.icon("info", size="24px").classes("text-purple-600")
                ui.label("ดูรายละเอียดเมนูและตัวเลือก").classes("text-lg font-bold")
            ui.button(
                "เปิดดูรายละเอียดเมนู",
                icon="visibility",
                on_click=detail_dialog.open,
            ).props("color=purple")

    with ui.footer().classes("bg-gray-100 text-gray-600 text-xs justify-center"):
        ui.label("© 2024 Food Order Demo — NiceGUI + SQLModel")


# =========================================================
# Entry Point
# =========================================================

if __name__ in {"__main__", "__mp_main__"}:
    create_db_and_tables()
    seed_if_empty()
    ui.run(
        title="Food Order Demo",
        favicon="🍽️",
        reload=False,
        port=8081,
        show=True,
    )
