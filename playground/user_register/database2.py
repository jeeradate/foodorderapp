from sqlmodel import create_engine, Session, select
from models2 import User

sqlite_url = f"sqlite:///database2.db"
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_tread": False})


def save_user_to_db(username_value: str, email_value: str):
    new_user = User(usernamme=username_value, email=email_value)
    with Session(engine) as session:
        session.add(new_user)
        session.commit()


def get_all_users_from_db():
    with Session(engine) as session:
        statement = select(User)
        return session.exec(statement).all
