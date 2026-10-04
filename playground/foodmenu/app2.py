from decimal import Decimal
from nicegui import ui
from sqlmodel import Session, select

from database import create_db_and_tables, engine
from models import Category, FoodItem

create_db_and_tables()

def get_categories()->list[Category]:
    with Session(engine) as session:
        statement = select(Category).order_by(Category.name)
        return list(session.exec(statement).all())

def get_food_items_by_category(category_id:int) -> list[FoodItem]:
    with Session(engine) as session:
        statement = (
            select(FoodItem)
            .where(FoodItem.category_id==category_id)
            .order_by(FoodItem.name)
        )    
        return list(session.exec(statement).all())

def get_category_options()->dict[int,str]:
    return{
        Category.id: category.name
        for category in get_categories() 
        if category.id in not None
    }    

@ui.refreshable
def show_menu_by_category()->None:
    get_categories =get_categories()
    if not categores:
        ui.label("No category yet")
        return
    for category in categoryies:
        
