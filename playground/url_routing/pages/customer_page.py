"""Customer Page Module

โมดูลสำหรับแสดงผลหน้าจอสั่งอาหารสำหรับลูกค้า
"""

from nicegui import ui


# ลงทะเบียน URL Route สำหรับหน้าลูกค้า (URL: /customer)
@ui.page("/customer")
def render_customer_page() -> None:
    """ฟังก์ชันแสดงผล UI หน้าลูกค้าเมื่อเข้าสู่ URL /customer"""
    with ui.column().classes("p-8 gap-4 max-w-xl mx-auto"):
        # ส่วน Header ของหน้า
        ui.label("📱 หน้าสั่งอาหารสำหรับลูกค้า").classes("text-2xl font-bold text-blue-600")
        ui.label("URL ปัจจุบันของคุณคือ: http://127.0.0.1:8081/customer").classes(
            "text-sm bg-gray-100 p-2 rounded"
        )

        # Mock Content ตัวอย่าง
        with ui.card().classes("w-full p-4"):
            ui.label("🍲 กระเพราหมูกรอบไข่ดาว").classes("text-lg font-semibold")
            ui.label("ราคา: 65 บาท").classes("text-gray-600")
            ui.button("➕ เพิ่มลงตะกร้า", color="primary").classes("mt-2")

        ui.separator().classes("my-4")

        # ปุ่มกดสำหรับเดินทางกลับหน้าหลัก (URL: /)
        ui.button(
            "🏠 กลับหน้าหลัก (Home)",
            on_click=lambda _: ui.navigate.to("/"),
            color="grey-7",
        )
