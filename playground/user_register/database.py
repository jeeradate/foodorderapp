from sqlmodel import create_engine, Session, select
from models import User  # Import Model มาใช้งานภายในฐานข้อมูล

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})


def save_user_to_db(username_value: str, email_value: str):
    """ฟังก์ชันสำหรับบันทึกข้อมูล User ใหม่ลง Database"""
    new_user = User(username=username_value, email=email_value)
    with Session(engine) as session:
        session.add(new_user)
        session.commit()


def get_all_users_from_db():
    """ฟังก์ชันสำหรับดึงข้อมูล User ทั้งหมดออกมาจาก Database"""
    with Session(engine) as session:
        statement = select(User)
        return session.exec(statement).all()
