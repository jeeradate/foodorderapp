"""Main Application Entry Point

ไฟล์หลักสำหรับกำหนด Page Routes และเริ่มต้นรัน NiceGUI Server
สั่งรันโปรแกรมด้วยคำสั่ง: python main.py
"""

from pathlib import Path
import sys

from nicegui import ui
from food_app.core.database import create_db_and_tables
from food_app.ui.components import render_header
from food_app.ui.pages.admin_page import render_admin_page
from food_app.ui.pages.customer_page import render_customer_page

# ---------------------------------------------------------
# Set Python Path ให้ชี้มาที่ Root Directory ของโปรเจกต์
# เพื่อป้องกันปัญหา ModuleNotFoundError / reportMissingImports
# ---------------------------------------------------------
ROOT_DIR: Path = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# =========================================================
# 1. Page Routing Definitions
# =========================================================


@ui.page("/")
def home_page() -> None:
    """หน้าหลัก (Navigation Hub / Main Menu) สำหรับเลือกเปิดไปยังหน้าต่างๆ"""
    render_header("หน้าหลัก (Main Menu)")

    with ui.column().classes("w-full max-w-4xl mx-auto p-6 items-center gap-6"):
        ui.label("🎯 ยินดีต้อนรับสู่ระบบ Food Order App").classes(
            "text-3xl font-bold text-gray-800 mt-4"
        )
        ui.label("กรุณาเลือกหน้าจอที่ต้องการจากปุมกลมด้านซ้ายบนสุด").classes("text-gray-600 mb-6")

        # Cards ตัวเลือกสำหรับนำทางไปยังหน้าต่างๆ
        with ui.row().classes("w-full gap-6 justify-center"):
            # Card หน้าสั่งอาหารลูกค้า
            with ui.card().classes(
                "w-80 p-6 flex flex-col items-center hover:shadow-lg transition-shadow cursor-pointer border"
            ):
                ui.icon("restaurant", size="64px", color="blue-6")
                ui.label("หน้าสั่งอาหารลูกค้า").classes("text-xl font-bold mt-4 mb-2")
                ui.label("สำหรับให้ลูกค้าเลือกดูรายการอาหารและสั่งซื้อ").classes(
                    "text-sm text-gray-500 text-center mb-4"
                )
                ui.button(
                    "เข้าสู่หน้าลูกค้า",
                    color="blue",
                    on_click=lambda: ui.navigate.to("/customer"),
                ).classes("w-full")

            # Card หน้า Admin จัดการ Master Data
            with ui.card().classes(
                "w-80 p-6 flex flex-col items-center hover:shadow-lg transition-shadow cursor-pointer border"
            ):
                ui.icon("admin_panel_settings", size="64px", color="green-6")
                ui.label("หน้า Admin (Master Data)").classes(
                    "text-xl font-bold mt-4 mb-2"
                )
                ui.label("สำหรับจัดการเมนูอาหาร หมวดหมู่ และโต๊ะ").classes(
                    "text-sm text-gray-500 text-center mb-4"
                )
                ui.button(
                    "เข้าสู่หน้า Admin",
                    color="green",
                    on_click=lambda: ui.navigate.to("/admin/master"),
                ).classes("w-full")


@ui.page("/customer")
def customer_route() -> None:
    """Route สำหรับหน้าสั่งอาหารสำหรับลูกค้า"""
    render_customer_page()


@ui.page("/admin/master")
def admin_route() -> None:
    """Route สำหรับหน้าผู้ดูแลระบบจัดการ Master Data"""
    render_admin_page()


# =========================================================
# 2. Application Startup
# =========================================================

if __name__ in {"__main__", "__mp_main__"}:
    # สร้างตารางใน Database SQLite หากยังไม่มีไฟล์ฐานข้อมูล
    create_db_and_tables()

    # สั่งเริ่มการทำงานของ NiceGUI Server
    ui.run(
        title="Food Order App",
        port=8081,
        reload=False,
        show=True,
    )
