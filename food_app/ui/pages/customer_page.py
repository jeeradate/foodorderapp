"""Customer Page Module

หน้าจอสำหรับลูกค้าใช้เลือกดูรายการอาหารและสั่งซื้อ
"""

from typing import Any
from nicegui import ui
from food_app.services.menu_service import get_all_categories, get_menus_by_category
from food_app.ui.components import render_header


def render_customer_page() -> None:
    """Render หน้าสั่งอาหารสำหรับลูกค้า"""
    render_header("หน้าสั่งอาหารสำหรับลูกค้า")

    with ui.column().classes("w-full max-w-5xl mx-auto p-4 gap-6"):
        ui.label("🛒 รายการอาหาร").classes("text-2xl font-bold text-gray-800")

        # ดึงข้อมูล Categories และ Menus มาแสดงผล
        categories: list[dict[str, Any]] = get_all_categories()
        menus: list[dict[str, Any]] = get_menus_by_category()

        # ส่วนแสดง Filter หมวดหมู่
        with ui.row().classes("gap-2"):
            ui.button("ทั้งหมด", color="primary").props("rounded")
            for cat in categories:
                ui.button(str(cat["name"]), color="grey-7").props("outline rounded")

        # ส่วนแสดงรายการเมนูอาหาร (Grid Layout)
        with ui.grid(columns=3).classes("w-full gap-4 mt-4"):
            for item in menus:
                with ui.card().classes(
                    "p-4 border shadow-sm flex flex-col justify-between"
                ):
                    ui.label(str(item["name"])).classes(
                        "text-lg font-bold text-gray-800"
                    )
                    ui.label(f"ราคา: {item['base_price']} บาท").classes(
                        "text-blue-600 font-semibold my-2"
                    )
                    ui.button("➕ เพิ่มในรายการ", color="green").props("w-full")
