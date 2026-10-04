# models.py
from decimal import Decimal
from typing import ClassVar, Optional

from sqlmodel import Field, Relationship, SQLModel


class Category(SQLModel, table=True):
    """ตารางหมวดหมู่อาหาร เช่น อาหารจานเดียว หรือ เครื่องดื่ม"""

    __tablename__: ClassVar[str] = "categories"

    # ก่อนบันทึกข้อมูล id เป็น None
    # หลังบันทึก database จะสร้าง id ให้อัตโนมัติ
    id: Optional[int] = Field(default=None, primary_key=True)

    # ชื่อหมวดหมู่ เช่น "เครื่องดื่ม"
    name: str

    # One-to-Many:
    # Category หนึ่งรายการ มี FoodItem ได้หลายรายการ
    food_items: list["FoodItem"] = Relationship(back_populates="category")


class FoodItem(SQLModel, table=True):
    """ตารางรายการอาหาร"""

    __tablename__: ClassVar[str] = "food_items"

    id: Optional[int] = Field(default=None, primary_key=True)

    # ชื่ออาหาร เช่น "ข้าวกะเพราหมูสับ"
    name: str

    # ราคาในหน่วยบาท; ตัวอย่างนี้ใช้ float เพื่อให้เข้าใจง่าย
    price: Decimal = Field(default=Decimal("0.00"), max_digits=6, decimal_places=2)

    # Foreign Key:
    # เชื่อม food_items.category_id ไปที่ categories.id
    category_id: int = Field(foreign_key="categories.id")

    # Many-to-One:
    # FoodItem หนึ่งรายการอยู่ใน Category เดียว
    category: Optional[Category] = Relationship(back_populates="food_items")
