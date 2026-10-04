# pages/home_page.py

from nicegui import ui


@ui.page("/")
def home_page() -> None:
    """หน้าแรกของระบบ"""

    with ui.column().classes("w-full max-w-2xl mx-auto p-6"):
        ui.label("Food Order App").classes("text-h3")
        ui.label("ตัวอย่าง NiceGUI + SQLModel + SQLite").classes("text-grey")

        ui.separator()

        with ui.row().classes("gap-4"):
            ui.button(
                "ดูเมนูอาหาร",
                on_click=lambda: ui.navigate.to("/menu"),
            ).props("color=primary")

            ui.button(
                "จัดการเมนู (Admin)",
                on_click=lambda: ui.navigate.to("/admin"),
            ).props("outline")
