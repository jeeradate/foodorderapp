"""Admin Page Module

โมดูลสำหรับแสดงผลหน้าจัดการระบบสำหรับ Admin
"""

from nicegui import ui


# ลงทะเบียน URL Route สำหรับหน้า Admin (URL: /admin)
@ui.page("/admin")
def render_admin_page() -> None:
    """ฟังก์ชันแสดงผล UI หน้าผู้ดูแลระบบเมื่อเข้าสู่ URL /admin"""
    with ui.column().classes("p-8 gap-4 max-w-xl mx-auto"):
        # ส่วน Header ของหน้า
        ui.label("⚙️ หน้าจัดการระบบ (Admin Dashboard)").classes(
            "text-2xl font-bold text-green-600"
        )
        ui.label("URL ปัจจุบันของคุณคือ: http://127.0.0.1:8081/admin").classes(
            "text-sm bg-gray-100 p-2 rounded"
        )

        # Mock Content ตัวอย่าง
        with ui.card().classes("w-full p-4"):
            ui.label("📊 สรุปยอดขายประจำวัน").classes("text-lg font-semibold")
            ui.label("ยอดขายรวมวันนี้: 1,250 บาท").classes("text-green-700 font-bold")

        ui.separator().classes("my-4")

        # ปุ่มกดสำหรับเดินทางกลับหน้าหลัก (URL: /)
        ui.button(
            "🏠 กลับหน้าหลัก (Home)",
            on_click=lambda _: ui.navigate.to("/"),
            color="grey-7",
        )
