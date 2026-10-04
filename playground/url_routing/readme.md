# ใน Directory นี้มีโปรแกรม สองโปรแกรม
- main.py 
- app.py
## main.py
สวัสดีครับนักเรียน! ครูยินดีเป็นอย่างยิ่งครับที่ได้ร่วมเดินทาง และเป็นที่ปรึกษาในการเรียนรู้ภาษา Python, SQLModel และ NiceGUI สำหรับโปรเจกต์ **Food Order App** ของคุณครับ

ครูขอชื่นชมในแนวทางการเรียนรู้ของคุณมากๆ ครับ การเน้นทำความเข้าใจ **Logic, Syntax, Type Hints** และโครงสร้างพื้นฐานให้แน่นก่อนที่จะขยับไปเรื่อง Class หรือความสวยงาม ถือเป็นรากฐานที่สำคัญที่สุดของการเป็นนักพัฒนาโปรแกรมที่ดี (Software Engineer) ครับ!

---

## 1. คำตอบสำหรับคำถามของคุณ (Explanation)

คำตอบสั้นๆ สำหรับคำถามของคุณคือ **"ไม่มีผลต่อการทำงานของโปรแกรมเลยครับ"**

คำสั่ง `# noqa: F401` ที่เราใส่ไว้ท้ายบรรทัด `import` นั้น ในทางภาษา Python เรียกว่า **Comment** ครับ ซึ่ง Python Interpreter (ตัวแปลภาษา Python) จะ **ข้าม (Ignore)** ข้อความทุกอย่างที่อยู่หลังเครื่องหมาย `#` ไปโดยสิ้นเชิง ทำให้ไม่มีผลต่อความเร็วหรือ Logical การทำงานของโค้ดแม้แต่น้อยครับ

### แล้วทำไมเราถึงต้องใส่ `# noqa: F401`?

สิ่งที่มีผลกับคำสั่งนี้ไม่ใช่ตัว Python ครับ แต่คือ **Linter Tool (ในที่นี้คือ Ruff / Flake8)** ที่ทำงานร่วมกับ VS Code ของคุณ:

1. **หน้าที่ของ Linter (Ruff):** Ruff คือเครื่องมือตรวจคุณภาพโค้ด มันจะคอยแสกนว่าคุณเขียนโค้ดผิดกฎมาตรฐาน PEP 8 หรือไม่
2. **กฎ F401 (Unused Import):** โดยปกติ ถ้าเรา `import` โมดูลเข้ามาแล้วไม่ได้เรียกชื่อโมดูลนั้นมาใช้งาน Ruff จะเตือนขึ้นมาทันทีว่า *F401: imported but unused* เพื่อเตือนให้เราลบโค้ดที่ไม่ใช้ออก


3. **กรณีพิเศษของ NiceGUI (`Side-Effect Import`):** ใน NiceGUI เราต้องการให้ Python **รันไฟล์ `customer_page.py**` เพื่อให้ Decorator `@ui.page` ทำงานลงทะเบียน URL Route แต่เราไม่ได้เรียกใช้ตัวแปรในไฟล์นั้นตรงๆ
4. **หน้าที่ของ `# noqa: F401`:** ย่อมาจาก **"No Quality Assurance for Rule F401"** เป็นการเขียนบอก Ruff ว่า *"ตรงนี้ผู้เขียนตั้งใจ Import เพื่อให้ Side Effect ทำงานนะ ไม่ต้องเตือน F401 ขึ้นมา!"* แถบ **Problems** ใน VS Code ของคุณจึงสะอาด ไม่มีเส้นยักสีเหลืองแจ้งเตือนนั่นเองครับ



---

## 2. ทฤษฎีที่ต้องทำความเข้าใจ (Core Theoretical Concepts)

### 1) Python Comments & Interpreter Execution

ในภาษา Python เครื่องหมาย `#` ใช้สำหรับสร้าง **Inline Comment** หรือ **Block Comment** ตัว Interpreter จะอ่านโค้ดทีละบรรทัด และเมื่อเจอเครื่องหมาย `#` มันจะหยุดอ่านบรรทัดนั้นทันที และข้ามไปอ่านบรรทัดถัดไป

```python
import pages.customer_page  # นี่คือ Comment ตัว Python จะมองเห็นแค่ 'import pages.customer_page'

```

### 2) Linter Directives (Pragmas / Inline Suppression)

เครื่องมือวิเคราะห์โค้ดแบบสถิต (Static Code Analysis Tools) เช่น Ruff, Flake8, Mypy หรือ Pylance จะอ่าน Comment พิเศษประเภท **Directives** เหล่านี้ เพื่อปรับเปลี่ยนพฤติกรรมการตรวจจับข้อผิดพลาด เช่น:

* `# noqa`: บอก Linter ไม่ให้เตือนทุกกฎในบรรทัดนั้น
* `# noqa: F401`: บอก Linter ละเว้นเฉพาะกฎ F401 (Unused Import)
* `# type: ignore`: บอก Mypy/Pylance ละเว้นการตรวจ Type Hint ในบรรทัดนั้น

---

## 3. Source Code ฉบับสมบูรณ์ทั้งไฟล์ (`playground/url_routing/main.py`)

ครูได้จัดทำโค้ดไฟล์ `main.py` ฉบับสมบูรณ์ พร้อม Comment อธิบายทุกแง่มุม และ Type Hints ที่ถูกต้องตามมาตรฐาน เพื่อให้นักเรียนคัดลอกไปวางทับไฟล์เดิมได้ทันทีครับ:

```python
"""Main Application Module (Central Router)

โมดูลหลักสำหรับรันระบบ ทำหน้าที่เป็นศูนย์รวม Routing และลงทะเบียน Page จากโมดูลอื่น ๆ
เน้นการเขียนแบบ Functional Style, มี Type Hints และละเว้นคำเตือน Linter อย่างถูกต้อง
"""

from typing import Any
from nicegui import ui

# ------------------------------------------------------------------------------
# Side-Effect Imports:
# การ Import ด้านล่างนี้ทำขึ้นเพื่อให้ Python อ่านไฟล์ และให้ @ui.page ในไฟล์เหล่านั้น
# ทำการลงทะเบียน URL Route เข้าสู่ระบบ NiceGUI
# คำสั่ง # noqa: F401 ท้ายบรรทัด เป็น Comment สั่ง Ruff (Linter) ให้ละเว้นการเตือน Unused Import
# โดยไม่มีผลกระทบต่อการทำงานของโปรแกรมในขณะ Runtime
# ------------------------------------------------------------------------------
import pages.admin_page  # noqa: F401
import pages.customer_page  # noqa: F401


@ui.page("/")
def render_home_page() -> None:
    """ฟังก์ชันแสดงผลหน้าหลัก (Root Path: /)

    ทำหน้าที่เป็นหน้าแรกของแอปพลิเคชัน บรรจุ Link และ ปุ่ม สำหรับนำทางไปยังส่วนอื่น ๆ
    """
    with ui.column().classes("p-8 gap-4 max-w-xl mx-auto"):
        # ส่วนแสดงหัวข้อหน้าหลัก
        ui.label("🍽️ ยินดีต้อนรับสู่ Food Order App").classes(
            "text-3xl font-bold text-blue-600"
        )
        ui.label(
            "กรุณาเลือกหน้าที่ต้องการเข้าใช้งานจากตัวเลือกด้านล่าง:"
        ).classes("text-gray-600")

        ui.separator().classes("my-2")

        # ----------------------------------------------------------------------
        # วิธีที่ 1: การใช้องค์ประกอบ ui.link (HTML Anchor Tag <a>)
        # ----------------------------------------------------------------------
        ui.label(
            "1. ตัวอย่างการใช้ ui.link (คลิกข้อความเพื่อเปลี่ยนหน้า):"
        ).classes("font-bold")

        ui.link(
            "👉 ไปยังหน้าเลือกซื้ออาหารของลูกค้า (/customer)", "/customer"
        ).classes("text-blue-500 hover:underline text-lg")

        ui.link(
            "👉 ไปยังหน้าจัดการระบบของผู้ดูแล (/admin)", "/admin"
        ).classes("text-green-500 hover:underline text-lg")

        ui.separator().classes("my-2")

        # ----------------------------------------------------------------------
        # วิธีที่ 2: การใช้องค์ประกอบ ui.button ร่วมกับ Event Callback on_click
        # ----------------------------------------------------------------------
        ui.label("2. ตัวอย่างการใช้ ui.button + ui.navigate.to:").classes(
            "font-bold"
        )

        with ui.row().classes("gap-4"):
            # ใช้ lambda _: เพื่อรับ ClickEventArguments เข้ามาไว้ที่ _ (ตัวแปรไม่ใช้งาน)
            # แล้วสั่งให้ ui.navigate.to เปลี่ยนแปลง URL Route ไปยังหน้าที่ต้องการ
            ui.button(
                "📱 เข้าหน้าลูกค้า",
                on_click=lambda _: ui.navigate.to("/customer"),
                color="primary",
            )
            ui.button(
                "⚙️ เข้าหน้า Admin",
                on_click=lambda _: ui.navigate.to("/admin"),
                color="positive",
            )


# ตรวจสอบจุดเริ่มต้นการรันโปรแกรม (Entry Point)
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Food Order App - Learn Routing", port=8081, reload=True)

```

---

## 4. แหล่งศึกษาเพิ่มเติม (Recommended Resources)

1. **Ruff Official Documentation — Suppressing Warnings (`# noqa`)**
* **URL:** [https://docs.astral.sh/ruff/linter/#suppressing-warnings](https://www.google.com/search?q=https://docs.astral.sh/ruff/linter/%2523suppressing-warnings&utm_source=gemini)
* **ประเด็นน่าศึกษา:** ทำความเข้าใจวิธีการใช้ `# noqa` ในรูปแบบต่างๆ และการระบุรหัสกฎเฉพาะเจาะจงเพื่อควบคุม Linter ในโปรเจกต์ Python


2. **Real Python — Python Comments and Best Practices**
* **URL:** [https://realpython.com/python-comments-guide/](https://realpython.com/python-comments-guide/?utm_source=gemini)
* **ประเด็นน่าศึกษา:** อ่านหลักการเขียน Comment ที่ดี เมื่อไหร่ควรใส่ และเมื่อไหร่ไม่ควรใส่ เพื่อให้โค้ดอ่านง่ายตามมาตรฐานสากล


3. **YouTube Tutorial — Python Code Quality Tools (Ruff, Flake8 & Black)**
* **Search Keywords:** `python ruff linter tutorial vscode`
* **คลิปแนะนำ:** ค้นหาวิดีโอแนะนำการตั้งค่า Ruff ใน VS Code เพื่อช่วยตรวจจับ Bug และปรับแต่งสไตล์โค้ดอัตโนมัติ



หากนักเรียนนำโค้ดไปวางทับแล้วมีคำถาม หรือสงสัยเกี่ยวกับ Logic และ Syntax ส่วนไหนเพิ่มเติม ส่งโค้ดมาพูดคุยกับครูได้ตลอดเลยนะครับ! ครูพร้อมจะอธิบายทุกแง่มุมให้คุณเข้าใจอย่างถ่องแท้ครับ!

## app.py

## โครงสร้าง `pages/` สำหรับ Food Order App

ตัวอย่างนี้แยกเป็น 3 หน้า:
- **Home:** หน้าเริ่มต้น
- **Menu:** แสดงเมนูอาหารตาม Category
- **Admin:** เพิ่ม Category และ Food Item

```text
foodmenu/
├── app.py
├── database.py
├── models.py
├── services/
│   ├── __init__.py
│   └── food_service.py
└── pages/
    ├── __init__.py
    ├── home_page.py
    ├── menu_page.py
    └── admin_page.py
```

> ไฟล์ `__init__.py` ว่างได้ แต่ควรมีเพื่อบอก Python ว่า `pages` และ `services` เป็น package

---

## 1) `app.py`

หน้าที่ของไฟล์นี้คือเริ่มระบบ, สร้างตาราง และ import หน้าเพื่อให้ NiceGUI ลงทะเบียน routes

```python
# app.py

from nicegui import ui

from database import create_db_and_tables

# Import เพื่อให้ decorator @ui.page ในแต่ละไฟล์ทำการลงทะเบียน route
import pages.home_page  # noqa: F401
import pages.menu_page  # noqa: F401
import pages.admin_page  # noqa: F401


# สร้าง database และ tables หากยังไม่มี
create_db_and_tables()

# เริ่ม NiceGUI
ui.run(
    title="Food Order App",
    reload=False,
)
```

หลังรันแล้วจะมี URL ดังนี้:

| หน้า | URL |
|---|---|
| Home | `http://localhost:8080/` |
| Menu | `http://localhost:8080/menu` |
| Admin | `http://localhost:8080/admin` |

---

## 2) `services/food_service.py`

แยกคำสั่งติดต่อ database ออกจากหน้า UI เพื่อให้โค้ดเป็นระเบียบ

```python
# services/food_service.py

from sqlmodel import Session, select

from database import engine
from models import Category, FoodItem


def get_categories() -> list[Category]:
    """ดึง Category ทั้งหมดจาก database"""
    with Session(engine) as session:
        statement = select(Category).order_by(Category.name)
        return list(session.exec(statement).all())


def get_category_options() -> dict[int, str]:
    """
    สร้างข้อมูลสำหรับ ui.select

    ตัวอย่าง:
    {1: "อาหารจานเดียว", 2: "เครื่องดื่ม"}
    """
    return {
        category.id: category.name
        for category in get_categories()
        if category.id is not None
    }


def get_food_items_by_category(category_id: int) -> list[FoodItem]:
    """ดึง Food Item เฉพาะ Category ที่เลือก"""
    with Session(engine) as session:
        statement = (
            select(FoodItem)
            .where(FoodItem.category_id == category_id)
            .order_by(FoodItem.name)
        )
        return list(session.exec(statement).all())


def add_category(name: str) -> None:
    """เพิ่ม Category ใหม่"""
    with Session(engine) as session:
        category = Category(name=name)
        session.add(category)
        session.commit()


def add_food_item(name: str, price: float, category_id: int) -> None:
    """เพิ่มรายการอาหารใหม่"""
    with Session(engine) as session:
        food_item = FoodItem(
            name=name,
            price=price,
            category_id=category_id,
        )
        session.add(food_item)
        session.commit()
```

---

## 3) `pages/home_page.py`

หน้าแรก มีลิงก์ไปยัง Menu และ Admin

```python
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
```

---

## 4) `pages/menu_page.py`

แสดงรายการอาหารแยกตาม Category

```python
# pages/menu_page.py

from nicegui import ui

from services.food_service import (
    get_categories,
    get_food_items_by_category,
)


@ui.page("/menu")
def menu_page() -> None:
    """หน้าแสดงเมนูอาหารตาม Category"""

    with ui.column().classes("w-full max-w-2xl mx-auto p-6"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label("เมนูอาหาร").classes("text-h4")
            ui.button(
                "กลับหน้าหลัก",
                icon="home",
                on_click=lambda: ui.navigate.to("/"),
            ).props("flat")

        categories = get_categories()

        if not categories:
            ui.label("ยังไม่มีหมวดหมู่หรือรายการอาหาร").classes("text-grey")
            ui.button(
                "ไปเพิ่มข้อมูลในหน้า Admin",
                on_click=lambda: ui.navigate.to("/admin"),
            )
            return

        # วนลูปแสดง Category แต่ละกลุ่ม
        for category in categories:
            # Category ที่บันทึกใน database แล้วควรมี id เสมอ
            if category.id is None:
                continue

            with ui.card().classes("w-full"):
                ui.label(category.name).classes("text-h6")

                food_items = get_food_items_by_category(category.id)

                if not food_items:
                    ui.label("ยังไม่มีรายการอาหาร").classes("text-grey")
                    continue

                # แสดง Food Item ภายใน Category
                for food in food_items:
                    with ui.row().classes("w-full justify-between"):
                        ui.label(food.name)
                        ui.label(f"{food.price:.2f} บาท").classes("font-bold")
```

---

## 5) `pages/admin_page.py`

หน้านี้ใช้เพิ่ม Category และเพิ่ม Food Item

```python
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
```

---

## ลำดับการทำงาน

```text
app.py
  ├── create_db_and_tables()
  ├── import pages.home_page
  ├── import pages.menu_page
  ├── import pages.admin_page
  └── ui.run()

ผู้ใช้เปิด /
  └── home_page() ถูกเรียก

ผู้ใช้เปิด /admin
  └── admin_page() ถูกเรียก
      └── บันทึก Category หรือ FoodItem ผ่าน food_service.py

ผู้ใช้เปิด /menu
  └── menu_page() อ่าน Category และ FoodItem จาก SQLite
```

## จุดสำคัญ

- `app.py` ไม่ควรวาง UI หลักของหน้าใดหน้าหนึ่ง
- ในแต่ละไฟล์หน้า ให้สร้าง UI **ภายใน function ที่มี `@ui.page()`** เท่านั้น
- `pages/` รับผิดชอบหน้าจอและการนำทาง
- `services/` รับผิดชอบการอ่าน/เขียนฐานข้อมูล
- `models.py` รับผิดชอบโครงสร้างตาราง
- `database.py` รับผิดชอบ engine และ `create_all()`

เมื่อทดลองเสร็จ ให้เปิด `/admin` เพิ่มข้อมูลก่อน แล้วไปที่ `/menu` เพื่อดูรายการอาหารตามหมวดหมู่ครับ

ขั้นต่อไปที่เหมาะคือเพิ่มหน้า Admin สำหรับ **แสดงตารางเมนู พร้อมปุ่มลบและแก้ไข** ครับ



```python
# database.py

from pathlib import Path

from sqlmodel import SQLModel, create_engine


# ============================================================
# ตำแหน่งไฟล์ SQLite Database
# ============================================================

# Path ของโฟลเดอร์ที่เก็บไฟล์ database.py
# ตัวอย่าง:
# D:\foodorderapp\playground\foodmenu
BASE_DIR = Path(__file__).resolve().parent

# ให้เก็บ database ไว้ใน:
# foodmenu/data/food_order.db
DATABASE_PATH = BASE_DIR / "data" / "food_order.db"

# สร้างโฟลเดอร์ data อัตโนมัติ หากยังไม่มี
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

# SQLite URL:
# ใช้ as_posix() เพื่อเปลี่ยน path Windows จาก \ เป็น /
# ตัวอย่าง: sqlite:///D:/foodorderapp/playground/foodmenu/data/food_order.db
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"


# ============================================================
# สร้าง SQLModel Engine
# ============================================================

# check_same_thread=False:
# เหมาะเมื่อใช้ SQLite ร่วมกับ web application เช่น NiceGUI
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# ============================================================
# สร้าง Database Tables
# ============================================================

def create_db_and_tables() -> None:
    """
    สร้างไฟล์ SQLite และตารางทั้งหมดที่ประกาศด้วย SQLModel

    ต้อง import models ก่อน เพื่อให้ SQLModel.metadata
    รู้จัก Category และ FoodItem ก่อนสั่ง create_all()
    """
    from models import Category, FoodItem  # noqa: F401

    SQLModel.metadata.create_all(engine)
```

ไฟล์ database จะถูกสร้างที่:

```text
D:\foodorderapp\playground\foodmenu\data\food_order.db
```

และใน `app.py` ให้เรียกใช้แบบนี้:

```python
from database import create_db_and_tables

create_db_and_tables()
```

ต้องการให้ผมส่ง `models.py` เวอร์ชันที่เข้าคู่กับ `database.py` นี้อีกครั้งด้วยไหมครับ?

```python
# models.py

from typing import ClassVar, Optional

from sqlmodel import Field, Relationship, SQLModel


# ============================================================
# ตาราง Category
# ============================================================

class Category(SQLModel, table=True):
    """
    ตารางหมวดหมู่อาหาร

    ตัวอย่างข้อมูล:
    - อาหารจานเดียว
    - ของทานเล่น
    - เครื่องดื่ม
    """

    # ชื่อตารางใน SQLite database
    __tablename__: ClassVar[str] = "categories"

    # Primary Key:
    # ก่อนบันทึกข้อมูล id จะเป็น None
    # หลังบันทึก SQLite จะสร้าง id เป็น 1, 2, 3, ... ให้อัตโนมัติ
    id: Optional[int] = Field(default=None, primary_key=True)

    # ชื่อหมวดหมู่ เช่น "เครื่องดื่ม"
    name: str

    # One-to-Many Relationship:
    # Category 1 รายการ มี FoodItem ได้หลายรายการ
    #
    # ตัวอย่าง:
    # category.food_items
    #
    # จะได้ list ของ FoodItem ที่อยู่ใน Category นี้
    food_items: list["FoodItem"] = Relationship(back_populates="category")


# ============================================================
# ตาราง FoodItem
# ============================================================

class FoodItem(SQLModel, table=True):
    """
    ตารางรายการอาหาร

    ตัวอย่างข้อมูล:
    - ชื่อ: ข้าวกะเพราหมูสับ
    - ราคา: 65.00
    - category_id: 1
    """

    # ชื่อตารางใน SQLite database
    __tablename__: ClassVar[str] = "food_items"

    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)

    # ชื่อรายการอาหาร
    name: str

    # ราคาเป็นหน่วยบาท
    # ตัวอย่างนี้ใช้ float เพื่อให้เข้าใจง่าย
    #
    # สำหรับระบบจริง แนะนำเก็บเป็น int หน่วยสตางค์
    # เช่น 65 บาท = 6500 สตางค์
    price: float

    # Foreign Key:
    # เชื่อม column food_items.category_id
    # ไปยัง column categories.id
    category_id: int = Field(foreign_key="categories.id")

    # Many-to-One Relationship:
    # FoodItem 1 รายการ สังกัด Category ได้ 1 รายการ
    #
    # ตัวอย่าง:
    # food_item.category
    #
    # จะได้ Category ของเมนูอาหารนี้
    category: Optional[Category] = Relationship(back_populates="food_items")
```

ให้วางไฟล์นี้ไว้ระดับเดียวกับ `app.py` และ `database.py`:

```text
foodmenu/
├── app.py
├── database.py
├── models.py
├── pages/
│   ├── __init__.py
│   ├── home_page.py
│   ├── menu_page.py
│   └── admin_page.py
├── services/
│   ├── __init__.py
│   └── food_service.py
└── data/
    └── food_order.db
```

จากนั้น `database.py` จะ import `Category` และ `FoodItem` เพื่อสร้างตาราง ส่วน `services/food_service.py` จะ import model ทั้งสองตัวเพื่ออ่านและบันทึกข้อมูลครับ

ต้องการให้ผมส่ง `services/food_service.py` เวอร์ชันพร้อมคอมเมนต์ที่ใช้คู่กับ `models.py` นี้ด้วยไหมครับ?