"""Main Application Module (Central Router)

ไฟล์หลักสำหรับรันระบบ ทำหน้าที่เป็นศูนย์รวม Routing และลงทะเบียน Page จากโมดูลอื่น ๆ
"""

from nicegui import ui

# ------------------------------------------------------------------------------
# CRITICAL CONCEPT: Side-Effect Imports
# เราใส่ # noqa: F401 ไว้ท้ายบรรทัด เพื่อบอก Linter (Ruff) ว่าเราตั้งใจ Import
# เพื่อให้ Decorator @ui.page ในไฟล์ปลายทางทำงาน (Side Effect) ไม่ใช่เพราะเขียนโค้ดค้างไว้
# ------------------------------------------------------------------------------
import pages.admin_page  # noqa: F401
import pages.customer_page  # noqa: F401


@ui.page("/")
def home_page() -> None:
    """ฟังก์ชันแสดงผลหน้าหลัก (URL: /)

    บรรจุ ลิงก์ และ ปุ่ม สำหรับนำทางไปยัง Route ของไฟล์อื่น
    """
    with ui.column().classes("p-8 gap-4 max-w-xl mx-auto"):
        ui.label("🍽️ ยินดีต้อนรับสู่ Food Order App").classes(
            "text-3xl font-bold text-blue-600"
        )
        ui.label("กรุณาเลือกหน้าที่ต้องการเข้าใช้งานจากด้านล่าง:").classes("text-gray-600")

        ui.separator().classes("my-2")

        ui.label("1. ตัวอย่างการใช้ ui.link (คลิกข้อความเพื่อเปลี่ยนหน้า):").classes("font-bold")
        ui.link("👉 ไปยังหน้าเลือกซื้ออาหารของลูกค้า (/customer)", "/customer").classes(
            "text-blue-500 no-underline hover:underline  text-lg"
        )
        ui.link("👉 ไปยังหน้าจัดการระบบของผู้ดูแล (/admin)", "/admin").classes(
            "text-green-500 hover:underline text-lg"
        )

        ui.separator().classes("my-2")

        ui.label("2. ตัวอย่างการใช้ ui.button + ui.navigate.to:").classes("font-bold")
        with ui.row().classes("gap-4"):
            ui.button(
                "📱 เข้าหน้าลูกค้า",
                on_click=lambda: ui.navigate.to("/customer"),
                color="primary",
            )
            ui.button(
                "⚙️ เข้าหน้า Admin",
                on_click=lambda _: ui.navigate.to("/admin"),
                color="positive",
            )


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Food Order App - Learn Routing", port=8081, reload=True)
