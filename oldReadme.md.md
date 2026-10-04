
# 📘 Architecture Blueprint & Knowledge Guide: Food Order App
> **Stack:** Python 3.11+ | SQLModel | NiceGUI | SQLite  
> **เป้าหมาย:** สรุปหลักการออกแบบระบบ (System Design), โครงสร้างโปรเจกต์ (Project Structure), ทฤษฎีที่ต้องรู้ และ Source Code ฉบับ Refactored สมบูรณ์

---

## 1. วิเคราะห์และตรวจทานภาพรวมระบบ (Analysis & Refactoring)

จากการตรวจทานข้อกำหนดเดิมของระบบ **Food Order App** พบว่ามี Domain Logic ที่ดีมากแล้ว แต่จำเป็นต้องปรับแก้ไขในส่วนของ Tech Stack เพื่อให้โค้ดตรงตามมาตรฐาน Python ยุคใหม่:

### ✅ จุดเด่นของ Domain Logic (ออกแบบไว้ดีมาก)
1. **Multi-Order Per Table:** รองรับลูกค้าที่มาโต๊ะเดียวกันแต่แยกกันจ่าย (1 โต๊ะ มีได้หลาย Order)
2. **Kitchen Batching:** ห้องครัวสามารถรวมรายการเมนูที่เหมือนกัน (เช่น ข้าวผัด 3 จาน) เพื่อผัดพร้อมกันข้าม Order ได้ ช่วยเพิ่มประสิทธิภาพการทำงาน
3. **Data Snapshot Pattern:** เก็บบันทึก "ราคา" และ "ตัวเลือก (Options)" ณ เวลาที่สั่ง ลงใน `OrderItem` และ `OrderItemOption` โดยตรง ป้องกันไม่ให้ยอดเงินในอดีตเปลี่ยนแปลงเมื่อมีการปรับราคาเมนูในอนาคต

---

### ⚠️ จุดที่ต้องแก้ไขเชิงเทคนิค (Tech Stack Fixes)

1. **เปลี่ยนจาก SQLAlchemy Declarative มาเป็น SQLModel Pure Syntax:**
   * *ปัญหาเดิม:* มีการประกาศ `from sqlalchemy.orm import DeclarativeBase` และใช้ `Mapped[...]` ซึ่งเป็นการเขียน SQLAlchemy แบบดั้งเดิม
   * *แนวทางแก้ไข:* เปลี่ยนมาใช้ `SQLModel` เป็น Base Class หลัก (`class Menu(SQLModel, table=True):`) ซึ่งผสมผสาน Pydantic (Validation & Type Hints) และ SQLAlchemy (ORM) เข้าด้วยกัน ทำให้เขียนง่าย ไร้ความซ้ำซ้อน และได้ Type Hint ที่ Pylance/Mypy อ่านเข้าใจง่าย

2. **ปรับ Directory Structure ให้เข้ากับ NiceGUI:**
   * *ปัญหาเดิม:* มีความสับสนระหว่าง `src layout` (`src/food_order_app/`) และ Root Package (`food_app/`)
   * *แนวทางแก้ไข:* จัดโครงสร้างโฟลเดอร์ให้ Package หลัก (`food_app/`) อยู่ระดับเดียวกับ `main.py` ที่ Root เพื่อป้องกันปัญหา Import Path (`ModuleNotFoundError`) และไม่ต้องคอยสั่ง `pip install -e .` ใหม่ทุกครั้งที่แก้ไฟล์

---

## 2. ทฤษฎีสำคัญที่ต้องทำความเข้าใจ (Core Theoretical Concepts)

### 1) Master Data vs Transaction Data
* **Master Data (ข้อมูลหลัก):** ข้อมูลที่ไม่ค่อยเปลี่ยนแปลง เช่น หมวดหมู่ (`Category`), เมนู (`Menu`), โซน (`Zone`), โต๊ะ (`DiningTable`)
* **Transaction Data (ข้อมูลธุรกรรม):** ข้อมูลที่เกิดขึ้นและเปลี่ยนแปลงตลอดเวลา เช่น ออเดอร์ (`FoodOrder`), รายการสั่ง (`OrderItem`), การชำระเงิน (`Payment`)
* *เหตุผลที่ต้องแยก:* การแยกไฟล์โมเดลเป็น `master.py` และ `transaction.py` ช่วยให้ค้นหาโค้ดง่าย และป้องกันปัญหา Circular Import (การดึงไฟล์ไปมาจนโปรแกรมพัง)

### 2) Separation of Concerns (Service Layer Pattern)
* **UI Layer (NiceGUI):** มีหน้าที่แสดงผล (Render) และรับ Input จากผู้ใช้เท่านั้น **ไม่ควรเขียน SQL Query ดึงฐานข้อมูลในหน้า UI โดยตรง**
* **Service Layer:** ทำหน้าที่ประมวลผล Business Logic และติดต่อกับ Database
* *ประโยชน์:* ทำให้โค้ดอ่านง่าย ตรวจสอบบั๊กได้ง่าย และหากต้องการเปลี่ยนเงื่อนไขธุรกิจในอนาคต จะแก้เพียงที่ `services/` จุดเดียว

### 3) Foreign Key Enforcement ใน SQLite
* โดยปกติ SQLite จะ **ปิด** การตรวจสอบ Foreign Key Constraint ไว้เป็น Default
* ใน `database.py` เราจึงต้องใช้ SQLAlchemy Event Listener สั่ง `PRAGMA foreign_keys=ON;` เมื่อเปิด Connection เพื่อให้ SQLite ตรวจสอบความถูกต้องของ Foreign Key เสมอ (เช่น ห้ามลบ Category หากยังมี Menu ใช้งานอยู่)

---

## 3. โครงสร้างโปรเจกต์ฉบับสมบูรณ์ (Project Directory Structure)

```text
food_order_app/
│
├── .venv/                   # Virtual Environment
├── .gitignore               # ไม่ Tracking ไฟล์ขยะ/DB
├── requirements.txt         # รายชื่อ Package ที่ต้องใช้
├── README.md                # คู่มือและเอกสารการออกแบบระบบ
├── main.py                  # Entry Point สำหรับเริ่มรัน NiceGUI
│
└── food_app/                # 📂 Package หลักของแอปพลิเคชัน
    ├── __init__.py
    ├── core/
    │   ├── __init__.py
    │   └── database.py      # SQLite Engine, Session Generator & Event Listener
    │
    ├── models/
    │   ├── __init__.py      # Export Models ทั้งหมด
    │   ├── base.py          # Helper Functions, Types และ FK Helpers
    │   ├── master.py        # Master Data (Category, Menu, Option, Zone, Table)
    │   └── transaction.py   # Transaction Data (Order, OrderItem, Batch, Payment)
    │
    ├── services/
    │   ├── __init__.py
    │   └── menu_service.py  # Business Logic จัดการข้อมูลเมนูอาหาร
    │
    └── ui/
        ├── __init__.py
        └── pages/
            ├── __init__.py
            └── admin_page.py # หน้า Dashboard/Admin ตัวอย่างสำหรับทดสอบ

```

---

## 4. โค้ดฉบับแก้ไขปรับปรุงสมบูรณ์ (Complete Source Code)

### 📄 `requirements.txt`

```text
nicegui>=2.0.0
sqlmodel>=0.0.16

```

### 📄 `.gitignore`

```gitignore
.venv/
__pycache__/
*.py[cod]
*.db
.DS_Store

```

---

### 📄 `food_app/core/database.py`

```python
"""Database Core Configuration Module

โมดูลจัดการการเชื่อมต่อฐานข้อมูล SQLite ร่วมกับ SQLModel
พร้อมการตั้งค่า Event Listener เพื่อเปิดใช้งาน Foreign Key Constraint ใน SQLite
"""

from pathlib import Path
from typing import Any, Generator

from sqlalchemy import event
from sqlmodel import Session, SQLModel, create_engine

# กำหนด Path สำหรับไฟล์ฐานข้อมูลให้อยู่ที่ Root ของโปรเจกต์
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
DB_FILE_PATH: Path = BASE_DIR / "food_order.db"
DATABASE_URL: str = f"sqlite:///{DB_FILE_PATH.as_posix()}"

# สร้าง Database Engine
# check_same_thread=False จำเป็นต้องใส่เมื่อใช้งานร่วมกับ Web Framework/NiceGUI
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)


@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(
    dbapi_connection: Any, connection_record: Any
) -> None:
    """บังคับให้ SQLite ตรวจสอบ Foreign Key Constraints ทุกครั้งที่มี Connection ใหม่"""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()


def create_db_and_tables() -> None:
    """สร้างตารางในฐานข้อมูลตาม Model ทั้งหมดที่ลงทะเบียนไว้"""
    import food_app.models  # noqa: F401 (Import เพื่อให้ SQLModel รู้จักตาราง)

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Generator Function สำหรับจัดการ Database Session"""
    with Session(engine) as session:
        yield session

```

---

### 📄 `food_app/models/base.py`

```python
"""Base Model Helpers & Utilities

ฟังก์ชันผู้ช่วยสำหรับ Data Models เช่น การดึงเวลา UTC และ Helper สำหรับสร้าง Foreign Key
"""

from datetime import datetime, timezone
from typing import Any, TypeVar, cast
from sqlmodel import Column, Field, ForeignKey, SQLModel

# Type Variable สำหรับรองรับ Generic Type ของ SQLModel
ModelT = TypeVar("ModelT", bound=SQLModel)


def utc_now() -> datetime:
    """คืนค่าเวลาปัจจุบันในรูปแบบ UTC (Timezone Aware)"""
    return datetime.now(timezone.utc)


def require_id(obj: ModelT) -> int:
    """ตรวจสอบและคืนค่า primary key 'id' ของ SQLModel instance

    Raises:
        RuntimeError: หากยังไม่มีค่า id (ลืมสั่ง session.commit หรือ session.flush)
    """
    obj_id: Any = getattr(obj, "id", None)
    if obj_id is None:
        raise RuntimeError(
            f"Model {type(obj).__name__} ยังไม่มี id! คุณลืมบันทึกลง Database หรือไม่?"
        )
    return cast(int, obj_id)


def fk_column(
    target: str,
    *,
    nullable: bool = False,
    ondelete: str = "RESTRICT",
) -> Any:
    """Helper สำหรับสร้าง Foreign Key Field พร้อมกำหนด RESTRICT/CASCADE ได้สะดวก"""
    return Field(
        default=None if nullable else ...,
        sa_column=Column(
            ForeignKey(target, ondelete=ondelete),
            nullable=nullable,
        ),
    )

```

---

### 📄 `food_app/models/master.py`

```python
"""Master Data Models

จัดเก็บโครงสร้างข้อมูลนิ่งของระบบ (Category, Menu, OptionGroup, MenuOption, Zone, DiningTable)
"""

from datetime import datetime
from decimal import Decimal
from typing import ClassVar, Optional
from sqlmodel import Field, SQLModel, UniqueConstraint

from food_app.models.base import fk_column, utc_now


class Category(SQLModel, table=True):
    """หมวดหมู่เมนูอาหาร"""

    __tablename__: ClassVar[str] = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True, index=True)
    description: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utc_now)


class OptionGroup(SQLModel, table=True):
    """กลุ่มตัวเลือกเพิ่มเติม (เช่น ระดับความเผ็ด, ปริมาณน้ำแข็ง)"""

    __tablename__: ClassVar[str] = "option_groups"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    allow_multiple: bool = Field(default=False)
    is_required: bool = Field(default=False)
    is_active: bool = Field(default=True)


class MenuOption(SQLModel, table=True):
    """ตัวเลือกย่อยของเมนู (เช่น เผ็ดมาก, หวาน 50%)"""

    __tablename__: ClassVar[str] = "menu_options"
    __table_args__ = (
        UniqueConstraint("option_group_id", "name", name="uq_option_group_name"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    option_group_id: int = fk_column("option_groups.id")
    name: str = Field(max_length=100)
    extra_price: Decimal = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2)
    is_active: bool = Field(default=True)


class MenuOptionLink(SQLModel, table=True):
    """ตารางเชื่อม Many-to-Many ระหว่าง Menu กับ OptionGroup"""

    __tablename__: ClassVar[str] = "menu_option_links"
    __table_args__ = (
        UniqueConstraint("menu_id", "option_group_id", name="uq_menu_option_group"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    menu_id: int = fk_column("menus.id", ondelete="CASCADE")
    option_group_id: int = fk_column("option_groups.id", ondelete="CASCADE")


class Menu(SQLModel, table=True):
    """รายการเมนูอาหาร"""

    __tablename__: ClassVar[str] = "menus"

    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: int = fk_column("categories.id")
    name: str = Field(index=True, max_length=150)
    description: Optional[str] = Field(default=None, max_length=500)
    base_price: Decimal = Field(max_digits=10, decimal_places=2)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utc_now)


class Zone(SQLModel, table=True):
    """โซนที่นั่งในร้านอาหาร (เช่น ห้องแอร์, ชั้น 2)"""

    __tablename__: ClassVar[str] = "zones"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True, index=True)
    description: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)


class DiningTable(SQLModel, table=True):
    """โต๊ะอาหาร (หมายเลขโต๊ะสามารถซ้ำกันได้หากอยู่ต่างโซนกัน)"""

    __tablename__: ClassVar[str] = "dining_tables"
    __table_args__ = (
        UniqueConstraint("zone_id", "table_number", name="uq_zone_table_number"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    zone_id: int = fk_column("zones.id")
    table_number: str = Field(max_length=20)
    seats: int = Field(default=4, ge=1)
    is_active: bool = Field(default=True)

```

---

### 📄 `food_app/models/transaction.py`

```python
"""Transaction Data Models

จัดเก็บโครงสร้างข้อมูลที่มีการเปลี่ยนแปลงตลอดเวลา (Order, OrderItem, Batch, Payment)
"""

from datetime import datetime
from decimal import Decimal
from typing import ClassVar, Optional
from sqlmodel import Field, SQLModel, UniqueConstraint

from food_app.models.base import fk_column, utc_now


class FoodOrder(SQLModel, table=True):
    """Order หลักสำหรับโต๊ะอาหาร"""

    __tablename__: ClassVar[str] = "food_orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_number: str = Field(max_length=30, unique=True, index=True)
    dining_table_id: int = fk_column("dining_tables.id")
    status: str = Field(default="draft", max_length=30)  # draft, confirmed, closed, cancelled
    note: Optional[str] = Field(default=None, max_length=500)
    opened_at: datetime = Field(default_factory=utc_now)
    confirmed_at: Optional[datetime] = Field(default=None)
    closed_at: Optional[datetime] = Field(default=None)


class OrderItem(SQLModel, table=True):
    """รายการอาหารย่อยภายใน Order (เก็บบันทึก Snapshot ราคา ณ วันที่สั่ง)"""

    __tablename__: ClassVar[str] = "order_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = fk_column("food_orders.id", ondelete="CASCADE")
    menu_id: int = fk_column("menus.id")

    # Snapshot Values
    menu_name_snapshot: str = Field(max_length=150)
    unit_price_snapshot: Decimal = Field(max_digits=10, decimal_places=2)

    quantity: int = Field(default=1, ge=1)
    status: str = Field(default="draft", max_length=30)  # draft, confirmed, cooking, ready, served, cancelled
    note: Optional[str] = Field(default=None, max_length=500)

    created_at: datetime = Field(default_factory=utc_now)
    confirmed_at: Optional[datetime] = Field(default=None)
    served_at: Optional[datetime] = Field(default=None)


class OrderItemOption(SQLModel, table=True):
    """Snapshot ของ Option ที่เลือกสำหรับ OrderItem นั้นๆ"""

    __tablename__: ClassVar[str] = "order_item_options"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_item_id: int = fk_column("order_items.id", ondelete="CASCADE")
    menu_option_id: Optional[int] = fk_column("menu_options.id", nullable=True)

    # Snapshot Values
    option_name_snapshot: str = Field(max_length=100)
    extra_price_snapshot: Decimal = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2)


class KitchenBatch(SQLModel, table=True):
    """ชุดการผลิตอาหารในครัว (สำหรับผัด/ปรุงพร้อมกันหลาย Order)"""

    __tablename__: ClassVar[str] = "kitchen_batches"

    id: Optional[int] = Field(default=None, primary_key=True)
    batch_key: str = Field(index=True, max_length=255)
    status: str = Field(default="cooking", max_length=30)  # cooking, completed
    created_at: datetime = Field(default_factory=utc_now)


class KitchenBatchItem(SQLModel, table=True):
    """ตารางเชื่อมระบุว่า KitchenBatch นี้นำมาจาก OrderItem รายการใดบ้าง"""

    __tablename__: ClassVar[str] = "kitchen_batch_items"
    __table_args__ = (
        UniqueConstraint("kitchen_batch_id", "order_item_id", name="uq_batch_item"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    kitchen_batch_id: int = fk_column("kitchen_batches.id", ondelete="CASCADE")
    order_item_id: int = fk_column("order_items.id", ondelete="CASCADE")


class Payment(SQLModel, table=True):
    """การชำระเงินของ Order"""

    __tablename__: ClassVar[str] = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = fk_column("food_orders.id", ondelete="CASCADE")
    payment_method: str = Field(max_length=30)  # cash, credit_card, qr_code
    amount: Decimal = Field(max_digits=10, decimal_places=2)
    paid_at: datetime = Field(default_factory=utc_now)

```

---

### 📄 `food_app/models/__init__.py`

```python
"""Models Package Exporter

รวบรวมและ Export Models ทั้งหมด เพื่อให้ SQLModel Metadata รับรู้และสร้างตารางได้ครบถ้วน
"""

from food_app.models.master import (
    Category,
    DiningTable,
    Menu,
    MenuOption,
    MenuOptionLink,
    OptionGroup,
    Zone,
)
from food_app.models.transaction import (
    FoodOrder,
    KitchenBatch,
    KitchenBatchItem,
    OrderItem,
    OrderItemOption,
    Payment,
)

__all__: list[str] = [
    "Category",
    "OptionGroup",
    "MenuOption",
    "MenuOptionLink",
    "Menu",
    "Zone",
    "DiningTable",
    "FoodOrder",
    "OrderItem",
    "OrderItemOption",
    "KitchenBatch",
    "KitchenBatchItem",
    "Payment",
]

```

---

### 📄 `food_app/services/menu_service.py`

```python
"""Menu Service Module

ให้บริการจัดการการดึงข้อมูลและเพิ่มข้อมูลเมนูอาหารสำหรับ UI Layer
"""

from decimal import Decimal
from typing import Any, Optional
from sqlmodel import Session, select

from food_app.core.database import engine
from food_app.models.master import Category, Menu


def get_all_categories() -> list[dict[str, Any]]:
    """ดึงข้อมูลหมวดหมู่ทั้งหมด"""
    with Session(engine) as session:
        statement = select(Category).where(Category.is_active == True)
        categories = session.exec(statement).all()
        return [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
            }
            for c in categories
        ]


def create_sample_data_if_empty() -> None:
    """สร้างข้อมูลตัวอย่าง หากในระบบยังไม่มีข้อมูล"""
    with Session(engine) as session:
        existing_cat = session.exec(select(Category)).first()
        if existing_cat is None:
            cat_main = Category(name="อาหารจานเดียว", description="เมนูผัด/ราดข้าว")
            cat_drink = Category(name="เครื่องดื่ม", description="น้ำดื่มและน้ำหวาน")
            session.add(cat_main)
            session.add(cat_drink)
            session.commit()

            session.refresh(cat_main)
            session.refresh(cat_drink)

            m1 = Menu(
                category_id=cat_main.id,  # type: ignore
                name="กระเพราหมูกรอบ",
                base_price=Decimal("65.00"),
            )
            m2 = Menu(
                category_id=cat_drink.id,  # type: ignore
                name="ชาไทยเย็น",
                base_price=Decimal("35.00"),
            )
            session.add(m1)
            session.add(m2)
            session.commit()


def get_menus_by_category(category_id: Optional[int] = None) -> list[dict[str, Any]]:
    """ดึงข้อมูลรายการอาหารตามหมวดหมู่"""
    with Session(engine) as session:
        statement = select(Menu).where(Menu.is_active == True)
        if category_id is not None:
            statement = statement.where(Menu.category_id == category_id)

        menus = session.exec(statement).all()
        return [
            {
                "id": m.id,
                "name": m.name,
                "base_price": float(m.base_price),
            }
            for m in menus
        ]

```

---

### 📄 `food_app/ui/pages/admin_page.py`

```python
"""Admin UI Page

หน้าจอ UI สำหรับแอดมินใช้ทดสอบดูข้อมูลในระบบ
"""

from nicegui import ui
from food_app.services.menu_service import (
    create_sample_data_if_empty,
    get_all_categories,
    get_menus_by_category,
)


def render_admin_page() -> None:
    """Render หน้าต่าง Dashboard สำหรับทดสอบการเชื่อมต่อ Database"""
    # สร้างข้อมูลเริ่มต้นทดสอบ
    create_sample_data_if_empty()

    ui.label("🍽️ ระบบบริหารจัดการร้านอาหาร (Food Order App)").classes("text-2xl font-bold mb-4")

    categories = get_all_categories()
    menus = get_menus_by_category()

    # Cards แสดงสถิติ
    with ui.row().classes("w-full gap-4 mb-6"):
        with ui.card().classes("flex-1 bg-blue-50 p-4"):
            ui.label("หมวดหมู่ทั้งหมด").classes("text-sm text-gray-600")
            ui.label(str(len(categories))).classes("text-3xl font-bold text-blue-700")

        with ui.card().classes("flex-1 bg-green-50 p-4"):
            ui.label("รายการอาหารทั้งหมด").classes("text-sm text-gray-600")
            ui.label(str(len(menus))).classes("text-3xl font-bold text-green-700")

    # Table แสดงเมนู
    ui.label("รายการเมนูอาหารในระบบ").classes("text-lg font-bold mb-2")
    columns = [
        {"name": "id", "label": "ID", "field": "id", "align": "left"},
        {"name": "name", "label": "ชื่อเมนู", "field": "name", "align": "left"},
        {"name": "base_price", "label": "ราคา (บาท)", "field": "base_price", "align": "right"},
    ]
    ui.table(columns=columns, rows=menus, row_key="id").classes("w-full")

```

---

### 📄 `main.py`

```python
"""Main Entry Point

ไฟล์หลักสำหรับสั่งเริ่มทำงานเซิร์ฟเวอร์ NiceGUI
สั่งรันด้วยคำสั่ง: python main.py
"""

from nicegui import ui
from food_app.core.database import create_db_and_tables
from food_app.ui.pages.admin_page import render_admin_page


@ui.page("/")
def main_page() -> None:
    """หน้าแรกของ Web Application"""
    ui.colors(primary="#2563eb")

    with ui.column().classes("w-full max-w-6xl mx-auto p-4"):
        render_admin_page()


if __name__ in {"__main__", "__mp_main__"}:
    # 1. สร้างตารางและฐานข้อมูล SQLite หากยังไม่มี
    create_db_and_tables()

    # 2. เริ่มเปิดเซิร์ฟเวอร์ NiceGUI
    ui.run(
        title="Food Order App",
        port=8081,
        reload=False,
        show=True,
    )



