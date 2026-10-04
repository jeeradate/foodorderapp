from typing import ClassVar, Optional
from sqlmodel import Field, Relationship, SQLModel


class Category(SQLModel, table=True):
    """ตารางเก็บหมวดหมู่อาหาร (เช่น เครื่องดื่ม, ของกินเล่น, อาหารจานเดียว)"""

    __tablename__: ClassVar[str] = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # ความสัมพันธ์ 1:N ไปยัง FoodItem
    food_items: list["FoodItem"] = Relationship(back_populates="category")


class FoodOption(SQLModel, table=True):
    """ตารางเก็บตัวเลือกเสริมของอาหาร (เช่น เพิ่มไข่ดาว +10 บาท, เผ็ดน้อย ฟรี)"""

    __tablename__: ClassVar[str] = "food_options"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    extra_price: float = Field(default=0.0)  # หากเป็น 0.0 หมายถึง ฟรี

    # Foreign Key เชื่อมโยงไปยัง FoodItem
    food_item_id: int = Field(foreign_key="food_items.id")
    food_item: Optional["FoodItem"] = Relationship(back_populates="options")


class FoodItem(SQLModel, table=True):
    """ตารางเก็บรายการอาหารหลัก"""

    __tablename__: ClassVar[str] = "food_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float

    # Foreign Key เชื่อมโยงไปยัง Category
    category_id: int = Field(foreign_key="categories.id")
    category: Optional[Category] = Relationship(back_populates="food_items")

    # ความสัมพันธ์ 1:N ไปยัง FoodOption
    options: list[FoodOption] = Relationship(
        back_populates="food_item",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
