"""Main Application Entry Point for Food Order App.

Central file defining Page Routes and launching the NiceGUI Web Server.
Command to run locally: python main.py
"""

from pathlib import Path
import sys
from typing import NoReturn

from icecream import ic
from nicegui import ui

from food_app.core.config import settings
from food_app.core.database import create_db_and_tables
from food_app.ui.components import render_header
from food_app.ui.pages.admin_page import render_admin_page
from food_app.ui.pages.customer_page import render_customer_page
from food_app.ui.pages.test_page import render_test_page

# ---------------------------------------------------------
# Set Python Path to Root Directory
# Ensures proper package import resolution across environments
# ---------------------------------------------------------
ROOT_DIR: Path = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# =========================================================
# 1. Page Routing Definitions
# =========================================================


@ui.page("/")
def home_page() -> None:
    """Navigation Hub / Main Menu for role selection."""
    render_header("หน้าหลัก (Main Menu)")

    with ui.column().classes("w-full max-w-4xl mx-auto p-6 items-center gap-6"):
        ui.label("🎯 ยินดีต้อนรับสู่ระบบ Food Order App").classes(
            "text-3xl font-bold text-gray-800 mt-4"
        )
        ui.label("กรุณาเลือกหน้าจอที่ต้องการจากปุ่มเมนูด้านล่าง").classes("text-gray-600 mb-6")
        ui.button("Test Page", on_click=lambda: ui.navigate.to("/test"))

        # Role Navigation Cards
        with ui.row().classes("w-full gap-6 justify-center"):
            # Customer Card
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

            # Admin Card
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
    """Route for customer food ordering interface."""
    render_customer_page()


@ui.page("/admin/master")
def admin_route() -> None:
    """Route for system administrator data management interface."""
    render_admin_page()


@ui.page("/test")
def test_route() -> None:
    """Route for system test page."""
    ic("Navigating to test page")
    render_test_page()


# =========================================================
# 2. Application Startup Logic
# =========================================================
def start_server() -> None:
    """Launches NiceGUI Web Server with settings provided from configuration."""
    ui.run(
        title=settings.APP_TITLE,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG_MODE,
        favicon="🍳",
    )


if __name__ in {"__main__", "__mp_main__"}:
    # Initialize SQLModel Database Tables
    create_db_and_tables()

    # Start NiceGUI Application
    start_server()
