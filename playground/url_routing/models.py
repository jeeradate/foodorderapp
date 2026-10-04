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
