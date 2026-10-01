"""UI Components Module

โมดูลสำหรับเก็บ UI Components ที่ใช้งานร่วมกันในหลายๆ หน้า เช่น Header และ Hamburger Navigation Menu
"""

from typing import Any
from nicegui import ui


def is_active_path(current_path: str, target_path: str) -> bool:
    """เปรียบเทียบ Path สองเส้นทางว่าคือหน้าเดียวกันหรือไม่ (Path Normalization)

    Args:
        current_path (str): Path ปัจจุบันที่ได้จาก Browser Context
        target_path (str): Path ที่ต้องการตรวจสอบ

    Returns:
        bool: คืนค่า True หากเป็น Path เดียวกัน
    """
    norm_current: str = current_path.rstrip("/")
    norm_target: str = target_path.rstrip("/")

    if norm_current == "" and norm_target == "":
        return True

    return norm_current == norm_target


def render_header(title: str) -> None:
    """สร้าง Header Bar พร้อม Hamburger Menu Dropdown สไตล์ Responsive

    Args:
        title (str): หัวข้อของหน้าที่กำลังแสดงผล
    """
    # 1. ดึง Path ปัจจุบันของ Browser จาก NiceGUI Context
    current_path: str = "/"
    try:
        page_obj: Any = getattr(ui.context.client, "page", None)
        if page_obj and hasattr(page_obj, "path"):
            current_path = str(page_obj.path)
    except Exception:
        current_path = "/"

    # 2. กำหนดโครงสร้างข้อมูลเมนู แยกตาม User Roles
    menu_groups: dict[str, list[tuple[str, str]]] = {
        "🛒 กลุ่มลูกค้า (Customer)": [
            ("🏠 หน้าหลักเมนูสั่งอาหาร", "/"),
            ("🛒 ตะกร้าสินค้า", "/customer/cart"),
            ("⏳ ติดตามสถานะอาหาร", "/order-status"),
        ],
        "📋 กลุ่มพนักงาน (Staff)": [
            ("📋 จัดการออเดอร์หน้าร้าน", "/staff/orders"),
        ],
        "🍳 กลุ่มห้องครัว/บาร์ (Kitchen)": [
            ("🍳 รายการที่ต้องทำ (KDS)", "/kitchen"),
        ],
        "⚙️ ผู้ดูแลระบบ (Admin)": [
            ("🍔 จัดการเมนูอาหาร", "/admin/menu"),
            ("🪑 จัดการโต๊ะอาหาร", "/admin/tables"),
            ("📊 รายงานยอดขาย", "/admin/reports"),
        ],
    }

    # 3. สร้าง UI Header Bar
    with ui.header().classes(
        "bg-blue-600 text-white flex justify-between items-center px-6 py-3 shadow-md"
    ):
        # ฝั่งซ้าย: แสดงชื่อระบบและชื่อหน้าปัจจุบัน
        ui.label(f"🍽️ Food Order App | {title}").classes("text-xl font-bold")

        # ฝั่งขวา: Hamburger Menu Button
        with ui.button(icon="menu", color="white").props(
            "flat round dense text-color=blue"
        ):
            # สร้าง Dropdown Menu ซ้อนไว้ภายในปุ่ม Hamburger
            with ui.menu().classes(
                "bg-white text-gray-800 shadow-xl rounded-lg p-2 min-w-[240px]"
            ):
                for group_name, items in menu_groups.items():
                    # แสดง Header ของแต่ละกลุ่ม Role
                    ui.label(group_name).classes(
                        "text-xs font-bold text-gray-400 px-3 pt-2 pb-1 uppercase tracking-wider"
                    )

                    for label_text, target_path in items:
                        is_active: bool = is_active_path(current_path, target_path)

                        if is_active:
                            # รายการหน้าปัจจุบัน: ไฮไลท์สีฟ้า ไอคอนเช็คถูก และกดซ้ำไม่ได้
                            with ui.menu_item().classes(
                                "bg-blue-50 text-blue-600 font-bold rounded-md"
                            ):
                                ui.label(f"✓ {label_text} (หน้าปัจจุบัน)").classes(
                                    "text-sm"
                                )
                        else:
                            # รายการหน้าอื่นๆ: ใช้ lambda _: ui.navigate.to(target_path)
                            # เพื่อรับ event arg มาไว้ที่ _ และส่ง target_path (str) ไปยัง ui.navigate.to
                            with ui.menu_item(
                                on_click=lambda _, path=target_path: ui.navigate.to(
                                    path
                                )
                            ).classes("hover:bg-gray-100 rounded-md transition-colors"):
                                ui.label(label_text).classes("text-sm text-gray-700")

                    # ใส่เส้นแบ่ง (Separator) คั่นระหว่างกลุ่ม
                    ui.separator().classes("my-1")
