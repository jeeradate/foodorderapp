# pages/admin_page.py

from nicegui import ui

from services.food_service import (
    add_category,
    add_food_item,
    get_category_options,
)


@ui.page("/admin")
def admin_page() -> None:
    """หน้า Admin สำหรับเพิ่มหมวดหมู่และรายการอาหาร"""

    with ui.column().classes("w-full max-w-2xl mx-auto p-6"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label("Admin: จัดการเมนู").classes("text-h4")
            ui.button(
                "กลับหน้าหลัก",
                icon="home",
                on_click=lambda: ui.navigate.to("/"),
            ).props("flat")

        # ====================================================
        # ส่วนเพิ่ม Category
        # ====================================================
        with ui.card().classes("w-full"):
            ui.label("เพิ่มหมวดหมู่อาหาร").classes("text-h6")

            category_name_input = ui.input(
                label="ชื่อหมวดหมู่",
                placeholder="เช่น อาหารจานเดียว",
            ).classes("w-full")

            def save_category() -> None:
                """ตรวจสอบและบันทึก Category"""
                name = (category_name_input.value or "").strip()

                if not name:
                    ui.notify("กรุณากรอกชื่อหมวดหมู่", type="warning")
                    return

                add_category(name)

                # ล้างข้อความที่กรอก
                category_name_input.value = ""
                category_name_input.update()

                # อัปเดตตัวเลือกใน dropdown เพิ่มอาหาร
                category_select.options = get_category_options()
                category_select.update()

                ui.notify(f'เพิ่มหมวดหมู่ "{name}" แล้ว', type="positive")

            ui.button(
                "เพิ่มหมวดหมู่",
                icon="add",
                on_click=save_category,
            ).props("color=primary")

        # ====================================================
        # ส่วนเพิ่ม Food Item
        # ====================================================
        with ui.card().classes("w-full"):
            ui.label("เพิ่มรายการอาหาร").classes("text-h6")

            food_name_input = ui.input(
                label="ชื่ออาหาร",
                placeholder="เช่น ข้าวกะเพราหมูสับ",
            ).classes("w-full")

            food_price_input = ui.number(
                label="ราคา (บาท)",
                min=0,
                format="%.2f",
            ).classes("w-full")

            # options มีรูปแบบ {id: ชื่อ Category}
            category_select = ui.select(
                options=get_category_options(),
                label="หมวดหมู่",
            ).classes("w-full")

            def save_food_item() -> None:
                """ตรวจสอบและบันทึก Food Item"""
                name = (food_name_input.value or "").strip()
                price = food_price_input.value
                category_id = category_select.value

                if not name:
                    ui.notify("กรุณากรอกชื่ออาหาร", type="warning")
                    return

                if price is None:
                    ui.notify("กรุณากรอกราคา", type="warning")
                    return

                if category_id is None:
                    ui.notify("กรุณาเลือกหมวดหมู่", type="warning")
                    return

                add_food_item(
                    name=name,
                    price=float(price),
                    category_id=int(category_id),
                )

                # ล้างค่าในฟอร์มหลังบันทึก
                food_name_input.value = ""
                food_name_input.update()

                food_price_input.value = None
                food_price_input.update()

                ui.notify(f'เพิ่มเมนู "{name}" แล้ว', type="positive")

            ui.button(
                "เพิ่มรายการอาหาร",
                icon="restaurant",
                on_click=save_food_item,
            ).props("color=primary")

        ui.separator()

        ui.button(
            "เปิดหน้าดูเมนูอาหาร",
            icon="menu_book",
            on_click=lambda: ui.navigate.to("/menu"),
        ).props("outline")
