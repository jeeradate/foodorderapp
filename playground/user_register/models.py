from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """Class นิยามโครงสร้างตารางของ User"""

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
