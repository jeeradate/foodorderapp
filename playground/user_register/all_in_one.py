from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select
from nicegui import ui

# ==========================================
# 1. Database Configuration & Engine
# ==========================================
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})


# ==========================================
# 2. Data Modeling
# ==========================================
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str


SQLModel.metadata.create_all(engine)


# ==========================================
# 3. Core Functions / Callbacks
# ==========================================
# ครูดำเปลี่ยนชื่อ Parameter เป็น refreshable_target เพื่อให้เข้าใจง่ายขึ้นครับ
def save_user(username_input, email_input, refreshable_target):
    if not username_input.value or not email_input.value:
        ui.notify("Please fill in all fields!", type="warning")
        return

    new_user = User(username=username_input.value, email=email_input.value)
    with Session(engine) as session:
        session.add(new_user)
        session.commit()

    # Clear Input Fields
    username_input.value = ""
    email_input.value = ""

    ui.notify("User saved successfully!", type="positive")

    # สั่ง Refresh ฟังก์ชันตารางโดยตรงอย่างถูกต้อง
    refreshable_target.refresh()


@ui.refreshable
def user_table():
    with Session(engine) as session:
        statement = select(User)
        users = session.exec(statement).all()

    columns = [
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "username", "label": "Username", "field": "username"},
        {"name": "email", "label": "Email", "field": "email"},
    ]
    ui.table(columns=columns, rows=[user.model_dump() for user in users], row_key="id")


# ==========================================
# 4. Web Page Definition
# ==========================================
@ui.page("/")
def main_page():
    ui.label("User Management System").classes("text-h4 q-my-md text-primary")

    with ui.card().classes("w-96 p-4 shadow-2"):
        ui.label("Add New User").classes("text-h6 q-mb-md")
        username = ui.input(label="Username").classes("w-full")
        email = ui.input(label="Email").classes("w-full")

        # กล่องสำหรับครอบ UI ตาราง
        table_box = ui.element("div").classes("w-full q-mt-md")
        with table_box:
            user_table()

        # จุดสำคัญ: ครูดำเปลี่ยนมาส่ง user_table เข้าไปตรงๆ แล้วครับ
        ui.button(
            "Save User", on_click=lambda: save_user(username, email, user_table)
        ).classes("w-full q-mt-md")


# ==========================================
# 5. Execution Guard
# ==========================================
if __name__ in {"__main__", "__mp_main__", "<run_path>"}:
    ui.run(port=8080)
