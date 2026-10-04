from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, ClassVar


class Category(SQLModel, table=True):
    __tablename__: ClassVar[str] = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str

    food_items: list["FoodItem"] = Relationship(back_populates="category")


class FoodItem(SQLModel, table=True):
    __tablename__: ClassVar[str] = "food_items"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str

    price: Decimal = Field(default=Decimal("0:00"), max_digits=6, decimal_places=2)

    category_id: int = Field(foreign_key="categories.id")

    category: Optional[Category] = Relationship(back_populates="food_items")
