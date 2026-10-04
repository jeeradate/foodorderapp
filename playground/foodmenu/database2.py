from pathlib import Path
from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine

BASE_DIR: Path = Path(__file__).resolve().parent

DATABASE_PATH: Path = BASE_DIR / "data" / "food_order2.db"
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
DATABASE_URL: str = f"sqlite:///{DATABASE_PATH.as_posix()}"
engine: Engine = create_engine(DATABASE_URL, connect_args={"check_same_tread": False})


def create_db_data_tables() -> None:
    SQLModel.metadata.create_all(engine)
