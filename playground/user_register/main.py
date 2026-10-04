from nicegui import ui
from sqlmodel import SQLModel
from database import engine, save_user_to_db, get_all_users_from_db

# สั่งสร้าง Table จากตรงนี้ โดยส่ง Engine ไปสั่งระบบ Metadata ตัวหลัก
SQLModel.metadata.create_all(engine)


# ==========================================
# Core Functions / Callbacks
# ==========================================
def handle_save(username_input, email_input, refreshable_target):
    if not username_input.value or not email_input.value:
        ui.notify("Please fill in all fields!", type="warning")
        return

    # เรียกใช้ฟังก์ชันบันทึกข้อมูลจากไฟล์ database.py
    save_user_to_db(username_input.value, email_input.value)

    # ล้างค่าหน้าจอ
    username_input.value = ""
    email_input.value = ""

    ui.notify("User saved successfully!", type="positive")
    refreshable_target.refresh()


@ui.refreshable
def user_table():
    # เรียกใช้ฟังก์ชันดึงข้อมูลจากไฟล์ database.py
    users = get_all_users_from_db()

    columns = [
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "username", "label": "Username", "field": "username"},
        {"name": "email", "label": "Email", "field": "email"},
    ]
    # แปลง Object เป็น Dictionary ด้วย model_dump() เหมือนเดิม
    ui.table(columns=columns, rows=[user.model_dump() for user in users], row_key="id")


# ==========================================
# Web Page Definition
# ==========================================
@ui.page("/")
def main_page():
    ui.label("User Management System").classes("text-h4 q-my-md text-primary")

    with ui.card().classes("w-96 p-4 shadow-2"):
        ui.label("Add New User").classes("text-h6 q-mb-md")
        username = ui.input(label="Username").classes("w-full")
        email = ui.input(label="Email").classes("w-full")

        table_box = ui.element("div").classes("w-full q-mt-md")
        with table_box:
            user_table()

        ui.button(
            "Save User", on_click=lambda: handle_save(username, email, user_table)
        ).classes("w-full q-mt-md")


# ==========================================
# Execution Guard
# ==========================================
if __name__ in {"__main__", "__mp_main__", "<run_path>"}:
    ui.run(port=8080)
