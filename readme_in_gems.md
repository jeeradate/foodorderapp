```markdown
# 📘 Architecture Blueprint & Knowledge Guide: Food Order App
> **Stack:** Python 3.11+ | SQLModel | NiceGUI | SQLite  
> **เป้าหมาย:** สรุปหลักการออกแบบระบบ (System Design), โครงสร้างโปรเจกต์ (Project Structure), ทฤษฎีที่ต้องรู้ และ Source Code ฉบับ Refactored สมบูรณ์

---

## 1. วิเคราะห์และตรวจทานภาพรวมระบบ (Analysis & Refactoring)

จากการตรวจทานข้อกำหนดเดิมของระบบ **Food Order App** พบว่ามี Domain Logic ที่ดีมากแล้ว แต่จำเป็นต้องปรับแก้ไขในส่วนของ Tech Stack เพื่อให้โค้ดตรงตามมาตรฐาน Python ยุคใหม่:

### ✅ จุดเด่นของ Domain Logic (ออกแบบไว้ดีมาก)
1. **Multi-Order Per Table:** รองรับลูกค้าที่มาโต๊ะเดียวกันแต่แยกกันจ่าย (1 โต๊ะ มีได้หลาย Order)
2. **Kitchen Batching:** ห้องครัวสามารถรวมรายการเมนูที่เหมือนกัน (เช่น ข้าวผัด 3 จาน) เพื่อผัดพร้อมกันข้าม Order ได้ ช่วยเพิ่มประสิทธิภาพการทำงาน
3. **Data Snapshot Pattern:** เก็บบันทึก "ราคา" และ "ตัวเลือก (Options)" ณ เวลาที่สั่ง ลงใน `OrderItem` และ `OrderItemOption` โดยตรง ป้องกันไม่ให้ยอดเงินในอดีตเปลี่ยนแปลงเมื่อมีการปรับราคาเมนูในอนาคต

---

### ⚠️ จุดที่ต้องแก้ไขเชิงเทคนิค (Tech Stack Fixes)

1. **เปลี่ยนจาก SQLAlchemy Declarative มาเป็น SQLModel Pure Syntax:**
   * *ปัญหาเดิม:* มีการประกาศ `from sqlalchemy.orm import DeclarativeBase` และใช้ `Mapped[...]` ซึ่งเป็นการเขียน SQLAlchemy แบบดั้งเดิม
   * *แนวทางแก้ไข:* เปลี่ยนมาใช้ `SQLModel` เป็น Base Class หลัก (`class Menu(SQLModel, table=True):`) ซึ่งผสมผสาน Pydantic (Validation & Type Hints) และ SQLAlchemy (ORM) เข้าด้วยกัน ทำให้เขียนง่าย ไร้ความซ้ำซ้อน และได้ Type Hint ที่ Pylance/Mypy อ่านเข้าใจง่าย

2. **ปรับ Directory Structure ให้เข้ากับ NiceGUI:**
   * *ปัญหาเดิม:* มีความสับสนระหว่าง `src layout` (`src/food_order_app/`) และ Root Package (`food_app/`)
   * *แนวทางแก้ไข:* จัดโครงสร้างโฟลเดอร์ให้ Package หลัก (`food_app/`) อยู่ระดับเดียวกับ `main.py` ที่ Root เพื่อป้องกันปัญหา Import Path (`ModuleNotFoundError`) และไม่ต้องคอยสั่ง `pip install -e .` ใหม่ทุกครั้งที่แก้ไฟล์

---

## 2. ทฤษฎีสำคัญที่ต้องทำความเข้าใจ (Core Theoretical Concepts)

### 1) Master Data vs Transaction Data
* **Master Data (ข้อมูลหลัก):** ข้อมูลที่ไม่ค่อยเปลี่ยนแปลง เช่น หมวดหมู่ (`Category`), เมนู (`Menu`), โซน (`Zone`), โต๊ะ (`DiningTable`)
* **Transaction Data (ข้อมูลธุรกรรม):** ข้อมูลที่เกิดขึ้นและเปลี่ยนแปลงตลอดเวลา เช่น ออเดอร์ (`FoodOrder`), รายการสั่ง (`OrderItem`), การชำระเงิน (`Payment`)
* *เหตุผลที่ต้องแยก:* การแยกไฟล์โมเดลเป็น `master.py` และ `transaction.py` ช่วยให้ค้นหาโค้ดง่าย และป้องกันปัญหา Circular Import (การดึงไฟล์ไปมาจนโปรแกรมพัง)

### 2) Separation of Concerns (Service Layer Pattern)
* **UI Layer (NiceGUI):** มีหน้าที่แสดงผล (Render) และรับ Input จากผู้ใช้เท่านั้น **ไม่ควรเขียน SQL Query ดึงฐานข้อมูลในหน้า UI โดยตรง**
* **Service Layer:** ทำหน้าที่ประมวลผล Business Logic และติดต่อกับ Database
* *ประโยชน์:* ทำให้โค้ดอ่านง่าย ตรวจสอบบั๊กได้ง่าย และหากต้องการเปลี่ยนเงื่อนไขธุรกิจในอนาคต จะแก้เพียงที่ `services/` จุดเดียว

### 3) Foreign Key Enforcement ใน SQLite
* โดยปกติ SQLite จะ **ปิด** การตรวจสอบ Foreign Key Constraint ไว้เป็น Default
* ใน `database.py` เราจึงต้องใช้ SQLAlchemy Event Listener สั่ง `PRAGMA foreign_keys=ON;` เมื่อเปิด Connection เพื่อให้ SQLite ตรวจสอบความถูกต้องของ Foreign Key เสมอ (เช่น ห้ามลบ Category หากยังมี Menu ใช้งานอยู่)

---

## 3. โครงสร้างโปรเจกต์ฉบับสมบูรณ์ (Project Directory Structure)

```text
food_order_app/
│
├── .venv/                   # Virtual Environment
├── .gitignore               # ไม่ Tracking ไฟล์ขยะ/DB
├── requirements.txt         # รายชื่อ Package ที่ต้องใช้
├── README.md                # คู่มือและเอกสารการออกแบบระบบ
├── main.py                  # Entry Point สำหรับเริ่มรัน NiceGUI
│
└── food_app/                # 📂 Package หลักของแอปพลิเคชัน
    ├── __init__.py
    ├── core/
    │   ├── __init__.py
    │   └── database.py      # SQLite Engine, Session Generator & Event Listener
    │
    ├── models/
    │   ├── __init__.py      # Export Models ทั้งหมด
    │   ├── base.py          # Helper Functions, Types และ FK Helpers
    │   ├── master.py        # Master Data (Category, Menu, Option, Zone, Table)
    │   └── transaction.py   # Transaction Data (Order, OrderItem, Batch, Payment)
    │
    ├── services/
    │   ├── __init__.py
    │   └── menu_service.py  # Business Logic จัดการข้อมูลเมนูอาหาร
    │
    └── ui/
        ├── __init__.py
        └── pages/
            ├── __init__.py
            └── admin_page.py # หน้า Dashboard/Admin ตัวอย่างสำหรับทดสอบ

```

---

