from decimal import Decimal
from typing import ClassVar, Optional
from sqlmodel import Field, Relationship, SQLModel


class Category(SQLModel, table=True):
    __tablename__: ClassVar[str] = "categories"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    food_items: list["FoodItem"] = Relationship(back_populates="category")


class FoodItem(SQLModel, table=True):
    __tablename__: ClassVar[str] = "food_item"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: Decimal = Field(default=Decimal("0.00"), max_digits=6, decimal_places=2)
    category_id: int = Field(foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="food_items")

class OrderedItem(SQLModel, table=True):
    __tablename__: ClassVar[str] = "ordered_item"
    id: Optional[int] = Field(default=None, primary_key=True)
    quantity:int
    food_item_id: int = Field(foreign_key="food_items.id")
    table_id:int = Field(foreign_key="tables.id")

class 
