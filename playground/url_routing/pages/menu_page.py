# pages/menu_page.py

from nicegui import ui

from services.food_service import (
    get_categories,
    get_food_items_by_category,
)


@ui.page("/menu")
def menu_page() -> None:
    """หน้าแสดงเมนูอาหารตาม Category"""

    with ui.column().classes("w-full max-w-2xl mx-auto p-6"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label("เมนูอาหาร").classes("text-h4")
            ui.button(
                "กลับหน้าหลัก",
                icon="home",
                on_click=lambda: ui.navigate.to("/"),
            ).props("flat")

        categories = get_categories()

        if not categories:
            ui.label("ยังไม่มีหมวดหมู่หรือรายการอาหาร").classes("text-grey")
            ui.button(
                "ไปเพิ่มข้อมูลในหน้า Admin",
                on_click=lambda: ui.navigate.to("/admin"),
            )
            return

        # วนลูปแสดง Category แต่ละกลุ่ม
        for category in categories:
            # Category ที่บันทึกใน database แล้วควรมี id เสมอ
            if category.id is None:
                continue

            with ui.card().classes("w-full"):
                ui.label(category.name).classes("text-h6")

                food_items = get_food_items_by_category(category.id)

                if not food_items:
                    ui.label("ยังไม่มีรายการอาหาร").classes("text-grey")
                    continue

                # แสดง Food Item ภายใน Category
                for food in food_items:
                    with ui.row().classes("w-full justify-between"):
                        ui.label(food.name)
                        ui.label(f"{food.price:.2f} บาท").classes("font-bold")
