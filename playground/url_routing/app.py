# app.py

from nicegui import ui

from database import create_db_and_tables

# Import เพื่อให้ decorator @ui.page ในแต่ละไฟล์ทำการลงทะเบียน route
import pages.home_page  # noqa: F401
import pages.menu_page  # noqa: F401
import pages.admin_page2  # noqa: F401


# สร้าง database และ tables หากยังไม่มี
create_db_and_tables()

# เริ่ม NiceGUI
ui.run(
    title="Food Order App",
    reload=False,
)
