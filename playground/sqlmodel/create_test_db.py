from sqlmodel import Field, SQLModel, Session, create_engine


# 1. นิยาม Model
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


# สร้าง SQLite Engine ใน Memory สำหรับทดสอบ
engine = create_engine("sqlite:///test.db")
SQLModel.metadata.create_all(engine)

# 2. การใช้งานจริง
with Session(engine) as session:
    # สร้าง Object ใหม่ ( id ยังเป็น None )
    new_hero: Hero = Hero(name="Deadpond", secret_name="Dive Wilson")
    print(f"ก่อน Save ลง DB -> id: {new_hero.id}")  # Output: None

    # บันทึกลง Database
    session.add(new_hero)
    session.commit()
    session.refresh(new_hero)

    # หลัง Save ( id จะถูกเปลี่ยนเป็น int ที่ส่งมาจาก Database )
    print(f"หลัง Save ลง DB  -> id: {new_hero.id}")  # Output: 1
    print(f"Type ของ id     -> {type(new_hero.id)}")  # Output: <class 'int'>
