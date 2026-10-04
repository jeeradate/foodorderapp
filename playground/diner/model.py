from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, ClassVar, Optional

from sqlalchemy.orm import Mapped
from sqlmodel import Column, Field, ForeignKey, Relationship, SQLModel, UniqueConstraint

# =========================================================
# Helper Functions
# =========================================================


def utc_now() -> datetime:
    """คืนค่าเวลาปัจจุบันแบบ UTC"""
    return datetime.now(timezone.utc)


def fk_column(
    target: str,
    *,
    nullable: bool = False,
    ondelete: str = "RESTRICT",
) -> Any:
    """
    สร้าง Foreign Key Column สำหรับ SQLModel
    รองรับ ondelete option ได้อย่างถูกต้อง
    """
    return Field(
        default=None if nullable else ...,
        sa_column=Column(
            ForeignKey(target, ondelete=ondelete),
            nullable=nullable,
        ),
    )


# =========================================================
# 1. Base / Dependent Models (เรียงลำดับเพื่อป้องกัน KeyError)
# =========================================================


class Category(SQLModel, table=True):
    """หมวดหมู่เมนู"""

    __tablename__: ClassVar[str] = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True, index=True)
    description: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utc_now)

    menus: Mapped[list["Menu"]] = Relationship(back_populates="category")


class OptionGroup(SQLModel, table=True):
    """กลุ่มตัวเลือกของอาหาร"""

    __tablename__: ClassVar[str] = "option_groups"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    allow_multiple: bool = Field(
        default=False,
        description="เลือกได้มากกว่า 1 Option หรือไม่",
    )
    is_required: bool = Field(
        default=False,
        description="บังคับให้เลือก Option หรือไม่",
    )
    is_active: bool = Field(default=True)

    options: Mapped[list["MenuOption"]] = Relationship(back_populates="option_group")


class MenuOption(SQLModel, table=True):
    """Option ของอาหาร"""

    __tablename__: ClassVar[str] = "menu_options"
    __table_args__ = (
        UniqueConstraint(
            "option_group_id",
            "name",
            name="uq_option_group_name",
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    option_group_id: int = fk_column("option_groups.id")
    name: str = Field(max_length=100)
    extra_price: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=10,
        decimal_places=2,
    )
    is_active: bool = Field(default=True)

    option_group: Mapped[Optional["OptionGroup"]] = Relationship(
        back_populates="options"
    )
    menu_links: Mapped[list["MenuOptionLink"]] = Relationship(
        back_populates="menu_option"
    )


class MenuOptionLink(SQLModel, table=True):
    """ตารางกลางเชื่อม Menu กับ MenuOption"""

    __tablename__: ClassVar[str] = "menu_option_links"
    __table_args__ = (
        UniqueConstraint(
            "menu_id",
            "menu_option_id",
            name="uq_menu_option",
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    menu_id: int = fk_column("menus.id")
    menu_option_id: int = fk_column("menu_options.id")

    menu: Mapped[Optional["Menu"]] = Relationship(back_populates="option_links")
    menu_option: Mapped[Optional["MenuOption"]] = Relationship(
        back_populates="menu_links"
    )


class Menu(SQLModel, table=True):
    """เมนูอาหารหลัก"""

    __tablename__: ClassVar[str] = "menus"

    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: int = fk_column("categories.id")
    name: str = Field(index=True, max_length=150)
    description: Optional[str] = Field(default=None, max_length=500)
    base_price: Decimal = Field(max_digits=10, decimal_places=2)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utc_now)

    category: Mapped[Optional["Category"]] = Relationship(back_populates="menus")
    option_links: Mapped[list["MenuOptionLink"]] = Relationship(back_populates="menu")
    order_items: Mapped[list["OrderItem"]] = Relationship(back_populates="menu")


class Zone(SQLModel, table=True):
    """โซนของร้านอาหาร"""

    __tablename__: ClassVar[str] = "zones"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True, index=True)
    description: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utc_now)

    tables: Mapped[list["DiningTable"]] = Relationship(back_populates="zone")


class DiningTable(SQLModel, table=True):
    """โต๊ะอาหาร"""

    __tablename__: ClassVar[str] = "dining_tables"
    __table_args__ = (
        UniqueConstraint(
            "zone_id",
            "table_number",
            name="uq_zone_table_number",
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    zone_id: int = fk_column("zones.id")
    table_number: str = Field(max_length=20)
    seats: int = Field(default=4, ge=1)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utc_now)

    zone: Mapped[Optional["Zone"]] = Relationship(back_populates="tables")
    orders: Mapped[list["FoodOrder"]] = Relationship(back_populates="dining_table")


# =========================================================
# 2. Transaction Models
# =========================================================


class OrderParticipant(SQLModel, table=True):
    """ผู้ร่วม Order"""

    __tablename__: ClassVar[str] = "order_participants"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = fk_column("food_orders.id", ondelete="CASCADE")
    display_name: str = Field(max_length=100)
    note: Optional[str] = Field(default=None, max_length=255)

    order: Mapped[Optional["FoodOrder"]] = Relationship(back_populates="participants")


class OrderStaff(SQLModel, table=True):
    """พนักงานที่เกี่ยวข้องกับ Order"""

    __tablename__: ClassVar[str] = "order_staff"
    __table_args__ = (
        UniqueConstraint(
            "order_id",
            "user_id",
            "duty",
            name="uq_order_staff_duty",
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = fk_column("food_orders.id", ondelete="CASCADE")
    user_id: int = fk_column("users.id")
    duty: str = Field(default="waiter", max_length=30)
    assigned_at: datetime = Field(default_factory=utc_now)

    order: Mapped[Optional["FoodOrder"]] = Relationship(back_populates="staff_links")
    user: Mapped[Optional["User"]] = Relationship(back_populates="order_staff_links")


class OrderItemOption(SQLModel, table=True):
    """Option ที่ลูกค้าเลือกให้ OrderItem"""

    __tablename__: ClassVar[str] = "order_item_options"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_item_id: int = fk_column("order_items.id", ondelete="CASCADE")
    menu_option_id: Optional[int] = fk_column("menu_options.id", nullable=True)
    option_name_snapshot: str = Field(max_length=100)
    extra_price_snapshot: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=10,
        decimal_places=2,
    )

    order_item: Mapped[Optional["OrderItem"]] = Relationship(back_populates="options")


class KitchenBatchItem(SQLModel, table=True):
    """ตารางเชื่อม KitchenBatch กับ OrderItem"""

    __tablename__: ClassVar[str] = "kitchen_batch_items"
    __table_args__ = (
        UniqueConstraint(
            "kitchen_batch_id",
            "order_item_id",
            name="uq_kitchen_batch_order_item",
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    kitchen_batch_id: int = fk_column("kitchen_batches.id", ondelete="CASCADE")
    order_item_id: int = fk_column("order_items.id", ondelete="CASCADE")
    quantity_in_batch: int = Field(default=1, ge=1)

    kitchen_batch: Mapped[Optional["KitchenBatch"]] = Relationship(
        back_populates="items"
    )
    order_item: Mapped[Optional["OrderItem"]] = Relationship(
        back_populates="kitchen_batch_items"
    )


class KitchenBatch(SQLModel, table=True):
    """ชุดงานที่ห้องครัวรวมรายการทำอาหารร่วมกัน"""

    __tablename__: ClassVar[str] = "kitchen_batches"

    id: Optional[int] = Field(default=None, primary_key=True)
    batch_key: str = Field(index=True, max_length=500)
    status: str = Field(default="waiting", max_length=30)
    created_at: datetime = Field(default_factory=utc_now)
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)

    items: Mapped[list["KitchenBatchItem"]] = Relationship(
        back_populates="kitchen_batch"
    )


class OrderItem(SQLModel, table=True):
    """รายการอาหารในแต่ละ Order"""

    __tablename__: ClassVar[str] = "order_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = fk_column("food_orders.id", ondelete="CASCADE")
    menu_id: int = fk_column("menus.id")
    menu_name_snapshot: str = Field(max_length=150)
    unit_price_snapshot: Decimal = Field(max_digits=10, decimal_places=2)
    quantity: int = Field(default=1, ge=1)
    status: str = Field(default="pending", max_length=30)
    note: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=utc_now)
    confirmed_at: Optional[datetime] = Field(default=None)
    prepared_at: Optional[datetime] = Field(default=None)
    served_at: Optional[datetime] = Field(default=None)

    order: Mapped[Optional["FoodOrder"]] = Relationship(back_populates="items")
    menu: Mapped[Optional["Menu"]] = Relationship(back_populates="order_items")
    options: Mapped[list["OrderItemOption"]] = Relationship(back_populates="order_item")
    kitchen_batch_items: Mapped[list["KitchenBatchItem"]] = Relationship(
        back_populates="order_item"
    )


class Payment(SQLModel, table=True):
    """ข้อมูลการชำระเงิน"""

    __tablename__: ClassVar[str] = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = fk_column("food_orders.id", ondelete="CASCADE")
    payment_method: str = Field(max_length=30)
    amount: Decimal = Field(max_digits=10, decimal_places=2)
    status: str = Field(default="paid", max_length=30)
    reference_no: Optional[str] = Field(default=None, max_length=100)
    paid_at: datetime = Field(default_factory=utc_now)

    order: Mapped[Optional["FoodOrder"]] = Relationship(back_populates="payments")


class FoodOrder(SQLModel, table=True):
    """Order หลักของลูกค้า"""

    __tablename__: ClassVar[str] = "food_orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_number: str = Field(max_length=30, unique=True, index=True)
    dining_table_id: int = fk_column("dining_tables.id")
    status: str = Field(default="draft", max_length=30)
    note: Optional[str] = Field(default=None)
    opened_at: datetime = Field(default_factory=utc_now)
    confirmed_at: Optional[datetime] = Field(default=None)
    closed_at: Optional[datetime] = Field(default=None)

    dining_table: Mapped[Optional["DiningTable"]] = Relationship(
        back_populates="orders"
    )
    participants: Mapped[list["OrderParticipant"]] = Relationship(
        back_populates="order"
    )
    staff_links: Mapped[list["OrderStaff"]] = Relationship(back_populates="order")
    items: Mapped[list["OrderItem"]] = Relationship(back_populates="order")
    payments: Mapped[list["Payment"]] = Relationship(back_populates="order")


class AuditLog(SQLModel, table=True):
    """เก็บประวัติการทำงานที่สำคัญ"""

    __tablename__: ClassVar[str] = "audit_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    actor_user_id: Optional[int] = fk_column(
        "users.id",
        nullable=True,
        ondelete="SET NULL",
    )
    entity_type: str = Field(max_length=50)
    entity_id: int
    action: str = Field(max_length=100)
    detail: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=utc_now)

    actor: Mapped[Optional["User"]] = Relationship(back_populates="audit_logs")


class User(SQLModel, table=True):
    """ผู้ใช้งานระบบ"""

    __tablename__: ClassVar[str] = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True, index=True)
    display_name: str = Field(max_length=100)
    role: str = Field(default="waiter", max_length=30)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utc_now)

    order_staff_links: Mapped[list["OrderStaff"]] = Relationship(back_populates="user")
    audit_logs: Mapped[list["AuditLog"]] = Relationship(back_populates="actor")
