"""Admin Master Data Page Module

หน้าจอสำหรับผู้ดูแลระบบใช้จัดการข้อมูลหลัก (Master Data) เช่น หมวดหมู่ และ เมนูอาหาร
"""

from typing import Any
from nicegui import ui
from food_app.services.menu_service import (
    create_sample_data_if_empty,
    get_all_categories,
    get_menus_by_category,
)
from food_app.ui.components import render_header


def render_admin_page() -> None:
    """Render หน้าจอจัดการ Master Data สำหรับ Admin"""
    render_header("จัดการข้อมูลหลัก (Master Data)")

    # สร้างข้อมูลตัวอย่างหากยังไม่มีใน DB
    create_sample_data_if_empty()

    categories: list[dict[str, Any]] = get_all_categories()
    menus: list[dict[str, Any]] = get_menus_by_category()

    with ui.column().classes("w-full max-w-5xl mx-auto p-4 gap-6"):
        ui.label("⚙️ เมนูจัดการ Master Data").classes("text-2xl font-bold text-gray-800")

        # Tab Navigation สำหรับแยกส่วนการจัดการ Master Data
        with ui.tabs().classes("w-full") as tabs:
            tab_menu = ui.tab("จัดการเมนูอาหาร")
            tab_category = ui.tab("จัดการหมวดหมู่")
            tab_table = ui.tab("จัดการโซน/โต๊ะ")

        with ui.tab_panels(tabs, value=tab_menu).classes(
            "w-full border p-4 rounded-b-lg"
        ):
            # Tab 1: จัดการเมนูอาหาร
            with ui.tab_panel(tab_menu):
                with ui.row().classes("justify-between items-center mb-4"):
                    ui.label("รายการเมนูอาหารทั้งหมด").classes("text-lg font-bold")
                    ui.button("➕ เพิ่มเมนูใหม่", color="primary")

                columns = [
                    {"name": "id", "label": "ID", "field": "id", "align": "left"},
                    {
                        "name": "name",
                        "label": "ชื่อเมนู",
                        "field": "name",
                        "align": "left",
                    },
                    {
                        "name": "base_price",
                        "label": "ราคา (บาท)",
                        "field": "base_price",
                        "align": "right",
                    },
                ]
                ui.table(columns=columns, rows=menus, row_key="id").classes("w-full")

            # Tab 2: จัดการหมวดหมู่
            with ui.tab_panel(tab_category):
                with ui.row().classes("justify-between items-center mb-4"):
                    ui.label("รายการหมวดหมู่ทั้งหมด").classes("text-lg font-bold")
                    ui.button("➕ เพิ่มหมวดหมู่ใหม่", color="primary")

                cat_columns = [
                    {"name": "id", "label": "ID", "field": "id", "align": "left"},
                    {
                        "name": "name",
                        "label": "ชื่อหมวดหมู่",
                        "field": "name",
                        "align": "left",
                    },
                    {
                        "name": "description",
                        "label": "คำอธิบาย",
                        "field": "description",
                        "align": "left",
                    },
                ]
                ui.table(columns=cat_columns, rows=categories, row_key="id").classes(
                    "w-full"
                )

            # Tab 3: จัดการโซนและโต๊ะอาหาร
            with ui.tab_panel(tab_table):
                ui.label("ส่วนจัดการโซนและโต๊ะอาหาร (กำลังพัฒนา)").classes(
                    "text-gray-500 italic"
                )
