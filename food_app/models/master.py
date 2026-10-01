"""Master Data Models

จัดเก็บโครงสร้างข้อมูลนิ่งของระบบ (Category, Menu, OptionGroup, MenuOption, Zone, DiningTable)
"""

from datetime import datetime
from decimal import Decimal
from typing import ClassVar, Optional
from sqlmodel import Field, SQLModel, UniqueConstraint

from food_app.models.base import fk_column, th_now


class Category(SQLModel, table=True):
    """หมวดหมู่เมนูอาหาร"""

    __tablename__: ClassVar[str] = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True, index=True)
    description: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=th_now)


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
    extra_price: Decimal = Field(
        default=Decimal("0.00"), max_digits=10, decimal_places=2
    )
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
    created_at: datetime = Field(default_factory=th_now)


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
