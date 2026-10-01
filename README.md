## แนวคิดระบบ Food Order App

Food Order App เป็นระบบเว็บสำหรับบริหารการสั่งอาหารภายในร้านอาหาร โดยสามารถมีหลายหน้าจอหรือหลายโมดูลที่ใช้งานร่วมกันบนฐานข้อมูลเดียว พัฒนาด้วย Python, SQLModel และ NiceGUI

ระบบรองรับการทำงานของพนักงานรับออเดอร์ ห้องครัว และแคชเชียร์ ตั้งแต่การเปิดออเดอร์ รับรายการอาหาร ติดตามสถานะการปรุง เสิร์ฟอาหาร จนถึงการชำระเงินและปิดออเดอร์

## โครงสร้างข้อมูลหลัก

- ร้านอาหารหนึ่งร้านมีได้หลาย โซน เช่น ห้องแอร์, ด้านนอก, ชั้น 2
- แต่ละโซนมีได้หลาย โต๊ะ
- หมายเลขโต๊ะสามารถซ้ำกันได้ หากอยู่คนละโซน เช่น โต๊ะ `1` ในโซนห้องแอร์ และโต๊ะ `1` ในโซนด้านนอก
- โต๊ะหนึ่งโต๊ะสามารถมีหลาย Order ที่เปิดพร้อมกันได้ เพื่อรองรับลูกค้าที่นั่งโต๊ะเดียวกันแต่สั่งอาหารและชำระเงินแยกกัน
- Order หนึ่งรายการสามารถมีผู้เกี่ยวข้องหลายคนได้ เช่น ลูกค้าหลายคนในกลุ่มเดียวกัน และพนักงานหรือบริกรที่รับคำสั่งซื้อ

## การสั่งอาหารและตัวเลือกเมนู

- แต่ละ Order สามารถมีรายการอาหารได้หลายรายการ
- รายการอาหารแต่ละรายการสามารถระบุ ตัวเลือกเพิ่มเติม (Options) ได้ เช่น
    - ระดับความเผ็ด: ไม่เผ็ด, เผ็ดน้อย, เผ็ดมาก
    - ขนาดหรือปริมาณ: ธรรมดา, พิเศษ, พิเศษมาก
    - วัตถุดิบเพิ่มเติม: เพิ่มเนื้อ, เพิ่มเครื่อง
    - เครื่องดื่ม: หวาน 50%, น้ำแข็ง, ไม่ใส่น้ำแข็ง
- Option แต่ละรายการอาจมีราคาเพิ่ม หรือไม่มีราคาเพิ่มก็ได้
- ระบบต้องบันทึกราคาของเมนูและ Option ณ เวลาที่สั่ง เพื่อให้ประวัติ Order ในอดีตไม่เปลี่ยนแปลงเมื่อมีการแก้ไขราคาเมนูภายหลัง

## การทำงานของห้องครัว

- ห้องครัวสามารถดูรายการอาหารที่ได้รับการยืนยันแล้ว และเลือกเปลี่ยนสถานะเป็น กำลังปรุง
- ห้องครัวสามารถรวมรายการเพื่อผลิตพร้อมกันได้ เมื่อเป็นเมนูเดียวกันและมี Option เหมือนกันทั้งหมด หรือไม่มี Option เช่น ข้าวผัดหมู 3 จานที่ไม่มีการปรับแต่ง ก็ผัดพร้อมกันเลย
- การรวมรายการสามารถเกิดข้าม Order ได้ เพื่อเพิ่มประสิทธิภาพและความรวดเร็วในการทำอาหาร
- แม้ระบบจะแสดงรายการรวมสำหรับห้องครัว แต่ต้องเก็บความเชื่อมโยงกลับไปยัง Order และรายการอาหารต้นทางเสมอ
- ห้องครัวควรจัดลำดับการทำอาหารตามเวลาที่ยืนยัน Order (`Confirmed At`) เป็นหลัก
- เป้าหมายคือทำให้รายการอาหารของแต่ละ Order เสร็จครบถ้วนโดยเร็วที่สุด

## สถานะของ Order และรายการอาหาร

ผู้สั่งอาหารและพนักงานสามารถติดตามสถานะของแต่ละรายการได้ โดยสถานะหลักประกอบด้วย

|สถานะ|ความหมาย|
|---|---|
|ร่างรายการ|กำลังเลือกอาหาร ยังไม่ส่งเข้าครัว|
|ยืนยันแล้ว|ยืนยัน Order และส่งรายการเข้าครัวแล้ว|
|กำลังปรุง|ห้องครัวรับรายการและเริ่มดำเนินการ|
|พร้อมเสิร์ฟ|ห้องครัวทำเสร็จ รอพนักงานนำไปเสิร์ฟ|
|เสิร์ฟแล้ว|พนักงานส่งอาหารถึงโต๊ะแล้ว|
|ยกเลิก|รายการถูกยกเลิก โดยควรเก็บเหตุผลและผู้ดำเนินการ|

ระบบควรแสดงรายการที่ยังค้างอยู่ของแต่ละ Order ได้อย่างชัดเจน เช่น รายการที่ยังไม่เริ่มทำ กำลังปรุง พร้อมเสิร์ฟ หรือยังไม่ได้เสิร์ฟ

## การชำระเงินและปิด Order

- คิดเงินแยกตาม Order แม้จะเป็นโต๊ะเดียวกัน
- ระบบคำนวณยอดจากราคาเมนู ราคา Option จำนวนรายการ ส่วนลด ภาษี และค่าบริการตามการตั้งค่าของร้าน
- ก่อนปิด Order ต้องตรวจสอบยอดชำระและบันทึกข้อมูลการชำระเงิน เช่น เงินสด, บัตรเครดิต หรือ QR Payment
- เมื่อชำระเงินครบแล้ว ระบบเปลี่ยนสถานะ Order เป็น ปิด Order
- Order ที่ปิดแล้วไม่ควรแก้ไขรายการอาหารหรือยอดเงินโดยตรง แต่ควรใช้กระบวนการคืนเงินหรือปรับปรุงรายการที่มีประวัติการดำเนินการชัดเจน

## ข้อเสนอแนะเพิ่มเติมสำหรับการออกแบบระบบ

- กำหนดสิทธิ์ผู้ใช้งานตามบทบาท เช่น ผู้ดูแลระบบ, พนักงานรับออเดอร์, ห้องครัว, พนักงานเสิร์ฟ และแคชเชียร์
- บันทึกประวัติการเปลี่ยนสถานะ รายการแก้ไข ยกเลิก และการชำระเงิน พร้อมผู้ดำเนินการและเวลา
- รองรับหมายเหตุพิเศษในระดับ Order และระดับรายการอาหาร เช่น “ลูกค้าแพ้อาหารทะเล”
- ออกแบบให้แต่ละหน้าจอใช้งานตามบทบาท เพื่อให้ข้อมูลไม่ซับซ้อนเกินจำเป็น
- ควรแยกข้อมูลหลัก เช่น เมนู, หมวดหมู่, Option, โซน และโต๊ะ ออกจากข้อมูลธุรกรรม เช่น Order, รายการอาหาร และการชำระเงิน

### Directory Structure ดังนี้:

1. Separation of Concerns (การแยกหน้าที่กันอย่างชัดเจน):

- Domain Data (Master vs Transaction): ข้อมูลนิ่ง เช่น Category, Menu, DiningTable (Master) ต้องแยกออกจากข้อมูลเดินหน้า เช่น FoodOrder, OrderItem, Payment (Transaction)

- UI Layer vs Data Access Layer: หน้าจอ NiceGUI ไม่ควรเขียน SQL Query เองตรงๆ แต่ควรดึงข้อมูลผ่าน Service/CRUD Layer เพื่อให้โค้ดทดสอบง่ายและอ่านง่าย

2. Multi-Role User Interface (หน้าจอแยกตามบทบาท):

- หน้า Ordering (เด็กเสิร์ฟ/ลูกค้าเปิดโต๊ะ)

- หน้า Kitchen Display System - KDS (ห้องครัว รวม Batch ผัดพร้อมกัน)

- หน้า Cashier (คิดเงิน/ปิด Order)

- หน้า Admin (จัดการเมนู โซน โต๊ะ)

3. Session Lifecycle ใน NiceGUI (Async Context):

- NiceGUI ทำงานแบบ Asynchronous และ Multi-client ดังนั้นการดึง Database Session ต้องระวังเรื่อง Thread Safety เราจึงควรมีโมดูล database.py กลางไว้ให้ทุกโมดูลดึงไปใช้ได้อย่างปลอดภัย


## แนวทางที่แนะนำ: `src layout` + Python package + Editable install

วิธีนี้เรียกว่า **Python Packaging แบบ `src layout`** และใช้ **editable install** (`pip install -e .`) ครับ

ผลลัพธ์คือคุณสามารถแยกโมดูลเป็นโฟลเดอร์ย่อยอย่างเป็นระเบียบ และ import ด้วยชื่อ package เช่น:

```python
from food_order_app.db.session import SessionLocal
from food_order_app.models.menu_item import MenuItem
```

โดยไม่ต้องเขียน path แบบ `../../...` หรือแก้ `sys.path` เอง ซึ่ง **ไม่แนะนำ** ครับ

## โครงสร้างโปรเจกต์

```text

food_order_app/
│
├── .venv/                   # Virtual Environment (มีอยู่แล้ว)
├── .env                     # ไฟล์เก็บ Configuration เช่น DATABASE_URL, SECRET_KEY
├── .gitignore               # ระบุไฟล์ที่ไม่ต้องการ Push ขึ้น Git (เช่น .venv, *.db)
├── requirements.txt         # รายชื่อ Package ที่ต้องใช้ (nicegui, sqlmodel, ฯลฯ)
├── README.md                # อธิบายโปรเจกต์และวิธีรัน
│
├── food_app/                # 📂 Package หลักของแอปพลิเคชัน
│   ├── __init__.py          # กำหนดให้โฟลเดอร์นี้เป็น Python Package
│   │
│   ├── core/                # 📂 ส่วนโครงสร้างพื้นฐาน (Core Engine)
│   │   ├── __init__.py
│   │   ├── config.py        # โหลดค่า Settings/Environment
│   │   └── database.py      # Engine, Session Factory, enable_foreign_keys
│   │
│   ├── models/              # 📂 Data Models (SQLModel Schemes)
│   │   ├── __init__.py      # Export ทุก Model เพื่อให้ create_all() รู้จัก
│   │   ├── base.py          # Helper Functions (เช่น utc_now, require_id)
│   │   ├── master.py        # Master Data: Category, Menu, Zone, DiningTable, OptionGroup
│   │   ├── transaction.py   # Transaction Data: FoodOrder, OrderItem, Payment, KitchenBatch
│   │   └── auth.py          # User, Role, AuditLog
│   │
│   ├── services/            # 📂 Data Access / Business Logic Layer (CRUD)
│   │   ├── __init__.py
│   │   ├── menu_service.py  # ดึงข้อมูลเมนู หมวดหมู่ ตัวเลือก
│   │   ├── order_service.py # เปิด Order, เพิ่มรายการ, คำนวณยอดเงิน
│   │   ├── kitchen_service.py # จัดลำดับ Queue, การจัดกลุ่ม Batch ทำอาหาร
│   │   └── payment_service.py # บันทึกการชำระเงิน, ปิด Order
│   │
│   └── ui/                  # 📂 User Interface Layer (NiceGUI Pages & Components)
│       ├── __init__.py
│       ├── components/      # UI Reusable Components (ชิ้นส่วนที่ใช้ซ้ำ)
│       │   ├── navbar.py    # แถบเมนูด้านบน
│       │   └── stats_card.py# การ์ดแสดงสถานะ
│       │
│       ├── pages/           # แต่ละหน้าตาม Role หรือ Module
│       │   ├── __init__.py
│       │   ├── admin_page.py   # หน้าจัดการเมนู/โต๊ะ
│       │   ├── pos_page.py     # หน้าเปิด Order และสั่งอาหาร (Waitstaff/POS)
│       │   ├── kitchen_page.py # หน้าจอห้องครัว (KDS)
│       │   └── cashier_page.py # หน้าคิดเงินและปิด Order
│       │
│       └── router.py        # ตัวจัดการ Route และ Layout รวมของ NiceGUI
│
├── seed.py                  # สคริปต์ใส่ข้อมูลทดสอบ (Seed Data)
└── main.py                  # Entry Point สำหรับรันโปรแกรม (ui.run)

```

> ทุกโฟลเดอร์ที่ต้องการให้ Python มองเป็น package ควรมี `__init__.py` แม้ไฟล์นั้นจะว่างเปล่าก็ตาม

## แยกหน้าที่ของแต่ละส่วน

| โฟลเดอร์/ไฟล์ | หน้าที่ |
|---|---|
| `pages/` | วางหน้าและ route ของ NiceGUI เช่น `/`, `/menu`, `/checkout` |
| `components/` | ส่วน UI ที่ใช้ซ้ำได้ เช่น navbar, ปุ่มเพิ่มลงตะกร้า, card อาหาร |
| `models/` | SQLAlchemy ORM model เช่น `MenuItem`, `Order`, `OrderItem` |
| `services/` | กฎธุรกิจและ CRUD เช่น เพิ่มเมนู, สร้าง order, คำนวณราคารวม |
| `db/` | การตั้งค่า SQLite, SQLAlchemy engine, session, Base และการสร้างตาราง |
| `schemas/` | รูปแบบข้อมูลเข้า/ออกจาก service; ยังไม่ต้องมีก็ได้ในระยะแรก |
| `tests/` | automated tests แยกออกจากโค้ดแอป |
| `pyproject.toml` | ระบุ dependencies และตั้งค่าให้ติดตั้ง package ได้ |

## 1) สร้าง Virtual Environment และติดตั้งโปรเจกต์

เปิด Terminal ที่โฟลเดอร์ `food-order-app`

```bash
python -m venv .venv
```

เปิดใช้งาน virtual environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**
```bat
.venv\Scripts\activate.bat
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

จากนั้นติดตั้งโปรเจกต์แบบ editable:

```bash
pip install -e ".[dev]"
```

คำสั่ง `-e` หมายถึง editable install: เมื่อแก้ไฟล์ใน `src/food_order_app/` แล้ว ไม่ต้องติดตั้งใหม่ทุกครั้ง

## 2) สร้าง `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "food-order-app"
version = "0.1.0"
description = "Food ordering application built with NiceGUI and SQLAlchemy"
requires-python = ">=3.11"
dependencies = [
    "nicegui",
    "sqlalchemy>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest",
    "ruff",
]

[tool.setuptools.packages.find]
where = ["src"]
```

ไฟล์นี้ทำให้ `pip install -e .` รู้ว่า package ของเราตั้งอยู่ใต้ `src/`

## 3) ตั้งค่าฐานข้อมูล SQLite

### `src/food_order_app/db/base.py`

```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

### `src/food_order_app/db/session.py`

```python
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "food_order.db"

DATABASE_PATH.parent.mkdir(exist_ok=True)

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}",
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
```

`check_same_thread=False` มีประโยชน์กับ SQLite เมื่อใช้ใน web application ซึ่งอาจมีการทำงานมากกว่าหนึ่ง thread

### `src/food_order_app/db/init_db.py`

```python
from food_order_app.db.base import Base
from food_order_app.db.session import engine

# import models เพื่อให้ SQLAlchemy รู้จักตารางทั้งหมด
from food_order_app.models import menu_item, order, order_item  # noqa: F401


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
```

## 4) ตัวอย่าง SQLAlchemy Models สำหรับ Food Order

### `src/food_order_app/models/menu_item.py`

```python
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from food_order_app.db.base import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    price: Mapped[int] = mapped_column()  # เก็บราคาเป็นหน่วยสตางค์
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
```

### `src/food_order_app/models/order.py`

```python
from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from food_order_app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(150))
    status: Mapped[str] = mapped_column(String(30), default="pending")

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )
```

### `src/food_order_app/models/order_item.py`

```python
from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from food_order_app.db.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"))

    quantity: Mapped[int] = mapped_column(default=1)
    unit_price: Mapped[int] = mapped_column()

    order: Mapped["Order"] = relationship(back_populates="items")
```

ความสัมพันธ์ของข้อมูลคือ:

```text
Order 1 รายการ
 └── มี OrderItem ได้หลายรายการ

OrderItem 1 รายการ
 └── อ้างอิง MenuItem 1 รายการ
```

## 5) สร้าง Service สำหรับแยก CRUD ออกจากหน้า UI

### `src/food_order_app/services/menu_service.py`

```python
from sqlalchemy import select

from food_order_app.db.session import SessionLocal
from food_order_app.models.menu_item import MenuItem


def get_available_menu_items() -> list[MenuItem]:
    with SessionLocal() as session:
        statement = (
            select(MenuItem)
            .where(MenuItem.is_available.is_(True))
            .order_by(MenuItem.name)
        )
        return list(session.scalars(statement).all())


def add_menu_item(name: str, price: int) -> MenuItem:
    with SessionLocal() as session:
        item = MenuItem(name=name, price=price)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
```

หลักสำคัญ: หน้า NiceGUI ไม่ควรมี SQL กระจัดกระจายเต็มไปหมด ให้หน้าเรียก `service` แทน เช่น `get_available_menu_items()`

## 6) จุดเริ่มต้น NiceGUI

### `src/food_order_app/main.py`

```python
from nicegui import ui

from food_order_app.db.init_db import create_tables
from food_order_app.pages import home, menu  # noqa: F401

create_tables()

ui.run(
    title="Food Order App",
    reload=True,
)
```

### `src/food_order_app/pages/home.py`

```python
from nicegui import ui


@ui.page("/")
def home_page() -> None:
    ui.label("Food Order App").classes("text-h4")
    ui.link("ดูเมนูอาหาร", "/menu")
```

### `src/food_order_app/pages/menu.py`

```python
from nicegui import ui

from food_order_app.services.menu_service import get_available_menu_items


@ui.page("/menu")
def menu_page() -> None:
    ui.label("เมนูอาหาร").classes("text-h4")

    for item in get_available_menu_items():
        with ui.card():
            ui.label(item.name)
            ui.label(f"{item.price / 100:.2f} บาท")
            ui.button("เพิ่มลงตะกร้า")
```

## 7) เพิ่ม `__main__.py` เพื่อสั่งรันแบบมาตรฐาน

### `src/food_order_app/__main__.py`

```python
from food_order_app.main import *  # noqa: F403
```

จาก root project ให้รัน:

```bash
python -m food_order_app
```

หรือจะรันโดยตรง:

```bash
python -m food_order_app.main
```

## 8) `.gitignore` ที่ควรมี

```gitignore
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
data/*.db
.env
```

ไม่ควร commit `.venv/`, cache และไฟล์ฐานข้อมูลที่เป็นข้อมูลทดสอบ/ข้อมูลส่วนตัวขึ้น Git

## สิ่งที่ไม่ควรทำ

- ไม่ควรใช้ `sys.path.append(...)` เพื่อให้ import ได้
- ไม่ควร import แบบ relative ที่ซับซ้อน เช่น `from ...db.session import SessionLocal`
- ไม่ควรวาง UI, SQLAlchemy model, SQL query และ business logic ไว้ใน `main.py` ไฟล์เดียว
- ไม่ควรใช้ `Base.metadata.create_all()` เป็นวิธีปรับโครงสร้างตารางในระบบที่เริ่มมีผู้ใช้แล้ว

เมื่อเริ่มมีการแก้ schema เช่น เพิ่ม column หรือเปลี่ยน relation ให้ใช้ **Alembic migrations** แทน `create_all()` ครับ

## แหล่งอ่านเพิ่มเติม

- โครงสร้าง `src layout` และเหตุผลที่ช่วยป้องกันปัญหา import: [python](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
- วิธีสร้าง Python package และตัวอย่างโครงสร้าง `pyproject.toml`: [python](https://packaging.python.org/tutorials/packaging-projects/)
- คู่มือเขียนและตั้งค่า `pyproject.toml`: [python](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- อธิบาย editable install และการใช้งาน `pip install -e`: [realpython](https://realpython.com/python-pyproject-toml/)
- เอกสาร NiceGUI หลัก: [nicegui](https://nicegui.io/documentation)
- NiceGUI เรื่อง pages และ routing: [nicegui](https://nicegui.io/documentation/section_pages_routing)
- SQLAlchemy ORM Quick Start: [sqlalchemy](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- SQLAlchemy Declarative Mapping สำหรับสร้าง model/table: [sqlalchemy](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html)

ถ้าคุณต้องการ ผมสามารถสร้าง **starter template แบบครบไฟล์** สำหรับ Food Order App นี้ พร้อมเมนูอาหาร ตะกร้า และการบันทึก Order ลง SQLite ให้คุณคัดลอกไปรันได้ทันทีครับ