from decimal import Decimal
from typing import Optional, Any
from icecream import ic
from sqlmodel import Session, select
from nicegui import ui

from database import create_db_and_tables, engine
from model import Category, Menu


def build_gui2() -> None:
    ui.label("Show Category & Menu").classes("text-2xl")


build_gui2()

ui.run(title="test")
