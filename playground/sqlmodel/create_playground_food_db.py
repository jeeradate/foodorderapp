import os
from typing import Optional
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

# บังคับให้สร้าง food_order.db ไว้ในโฟลเดอร์ playground เดียวกับตัวไฟล์ sample.py
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
DB_PATH: str = os.path.join(BASE_DIR, "playground_food.db")

sqlite_url: str = f"sqlite:///{DB_PATH}"
engine = create_engine(sqlite_url, echo=True)


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)

    items: list["FoodItem"] = Relationship(back_populates="category")


class FoodItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: float
    is_available: bool = Field(default=True)

    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="items")


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def add_sample_data() -> None:
    with Session(engine) as session:
        cat_drinks: Category = Category(name="Beverages")
        item1: FoodItem = FoodItem(
            name="Iced Green Tea", price=45.0, category=cat_drinks
        )

        session.add(cat_drinks)
        session.add(item1)
        session.commit()


def get_available_drinks() -> list[FoodItem]:
    with Session(engine) as session:
        statement = select(FoodItem).where(FoodItem.is_available == True)
        results = session.exec(statement)
        return list(results.all())


if __name__ == "__main__":
    create_db_and_tables()
    add_sample_data()
    drinks: list[FoodItem] = get_available_drinks()
    print(f"\nFound drinks: {drinks}")