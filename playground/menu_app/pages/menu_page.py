from nicegui import ui
from models import Category, FoodItem
from services.food_service import get_categories, get_food_item_by_category


@ui.refreshable
def render_menu_list() -> None:
    """ฟังก์ชัน Render เมนูอาหารพร้อม Option แสดงผลบนหน้าเว็บ"""
    categories: list[Category] = get_categories()

    if not categories:
        ui.label("No Category yet").classes("text-grey")
        ui.button("Goto Admin page", on_click=lambda _: ui.navigate.to("/admin"))
        return

    for category in categories:
        if category.id is None:
            continue

        with ui.card().classes("w-full my-2"):
            ui.label(category.name).classes("text-h6 text-primary")

            food_items: list[FoodItem] = get_food_item_by_category(category.id)

            if not food_items:
                ui.label("No food item yet").classes("text-grey")
                continue

            for food in food_items:
                with ui.column().classes("w-full py-2 border-b border-gray-100"):
                    # แถบแสดงชื่อและราคาหลัก
                    with ui.row().classes("w-full justify-between items-center"):
                        ui.label(food.name).classes("font-bold text-base")
                        ui.label(f"{food.price:.2f} Baht").classes(
                            "font-bold text-positive"
                        )

                    # แถบแสดง Options (ฟรี / มีราคา)
                    if food.options:
                        with ui.row().classes("w-full gap-1 items-center mt-1"):
                            ui.label("Options:").classes("text-xs text-gray-500")
                            for opt in food.options:
                                price_text: str = (
                                    "Free"
                                    if opt.extra_price == 0
                                    else f"+{opt.extra_price:.2f} B"
                                )
                                color_prop: str = (
                                    "green" if opt.extra_price == 0 else "blue"
                                )

                                ui.chip(
                                    f"{opt.name} ({price_text})",
                                    color=color_prop,
                                ).props("dense outline size=sm")


@ui.page("/menu")
def menu() -> None:
    """หน้าหลักสำหรับแสดงรายการเมนูอาหาร"""
    with ui.column().classes("w-full max-w-2xl mx-auto p-6"):
        with ui.row().classes("w-full items-center justify-between mb-4"):
            ui.label("Food Menu").classes("text-h4")

            with ui.row():
                ui.button(
                    icon="refresh",
                    on_click=render_menu_list.refresh,
                ).props("flat round").tooltip("Refresh")

                ui.button(
                    "Goto Admin",
                    on_click=lambda _: ui.navigate.to("/admin"),
                )
                ui.button(
                    "Home",
                    icon="home",
                    on_click=lambda _: ui.navigate.to("/"),
                ).props("color=primary")

        render_menu_list()
