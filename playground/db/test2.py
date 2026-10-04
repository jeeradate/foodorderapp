from pathlib import Path
from icecream import ic
from sqlmodel import SQLModel, Field, create_engine

ic("====== Start ======")
current_dir = Path(__file__).resolve().parents[0].as_posix()
ic(current_dir, type(current_dir))
# medel


# Database
