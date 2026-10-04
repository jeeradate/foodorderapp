from nicegui import ui
from models import Category
from services.food_service import get_categories, get_food_item_by_category


@ui.refreshable
def render_menu_list() -> None:
    """ฟังก์ชันสำหรับ render รายการ Category และ Food Items

    ใช้ @ui.refreshable เพื่อให้สั่ง Re-render UI ส่วนนี้ใหม่ได้ทันทีที่มีการเปลี่ยนแปลงข้อมูล
    """
    # ดึงข้อมูล Categories ล่าสุดจาก Database ทุกครั้งที่มีการ render
    categories: list[Category] = get_categories()

    if not categories:
        ui.label("No Category yet").classes("text-grey")
        ui.button(
            "Goto Admin",
            on_click=lambda _: ui.navigate.to("/admin"),
        )
        return

    # แสดงรายการ Category และอาหารภายในหมวดหมู่นั้น
    for category in categories:
        if category.id is None:
            continue

        with ui.card().classes("w-full"):
            ui.label(category.name).classes("text-h6")

            # ดึงรายการอาหารตาม Category ID
            food_items = get_food_item_by_category(category.id)

            if not food_items:
                ui.label("No food item yet").classes("text-grey")
                continue

            for food in food_items:
                with ui.row().classes("w-full justify-between"):
                    ui.label(food.name)
                    ui.label(f"{food.price:.2f} baht").classes("font-bold")


@ui.page("/menu")
def menu() -> None:
    """หน้าหลักสำหรับแสดงรายการเมนูอาหาร"""
    ui.label("Show Menu")

    with ui.column().classes("w-full max-w-2xl mx-auto p-6"):
        # Header และปุ่มนำทาง
        with ui.row().classes("w-full items-center justify-between"):
            ui.label("Food Menu").classes("text-h4")

            # ปุ่มสำหรับ Refresh หน้าจอด้วยตนเอง
            ui.button(
                icon="refresh",
                on_click=render_menu_list.refresh,
            ).props("flat round")

            ui.button(
                "Back to Home",
                icon="home",
                on_click=lambda _: ui.navigate.to("/"),
            ).props("color=primary")

        # เรียกใช้งาน UI component ที่สามารถ refresh ได้
        render_menu_list()
