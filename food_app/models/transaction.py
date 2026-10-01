"""Transaction Data Models

จัดเก็บโครงสร้างข้อมูลที่มีการเปลี่ยนแปลงตลอดเวลา (Order, OrderItem, Batch, Payment)
"""

from datetime import datetime
from decimal import Decimal
from typing import ClassVar, Optional
from sqlmodel import Field, SQLModel, UniqueConstraint

from food_app.models.base import fk_column, th_now


class FoodOrder(SQLModel, table=True):
    """Order หลักสำหรับโต๊ะอาหาร"""

    __tablename__: ClassVar[str] = "food_orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_number: str = Field(max_length=30, unique=True, index=True)
    dining_table_id: int = fk_column("dining_tables.id")
    status: str = Field(
        default="draft", max_length=30
    )  # draft, confirmed, closed, cancelled
    note: Optional[str] = Field(default=None, max_length=500)
    opened_at: datetime = Field(default_factory=th_now)
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
    status: str = Field(
        default="draft", max_length=30
    )  # draft, confirmed, cooking, ready, served, cancelled
    note: Optional[str] = Field(default=None, max_length=500)

    created_at: datetime = Field(default_factory=th_now)
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
    extra_price_snapshot: Decimal = Field(
        default=Decimal("0.00"), max_digits=10, decimal_places=2
    )


class KitchenBatch(SQLModel, table=True):
    """ชุดการผลิตอาหารในครัว (สำหรับผัด/ปรุงพร้อมกันหลาย Order)"""

    __tablename__: ClassVar[str] = "kitchen_batches"

    id: Optional[int] = Field(default=None, primary_key=True)
    batch_key: str = Field(index=True, max_length=255)
    status: str = Field(default="cooking", max_length=30)  # cooking, completed
    created_at: datetime = Field(default_factory=th_now)


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
    paid_at: datetime = Field(default_factory=th_now)
