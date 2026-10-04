from typing import Any
from nicegui import ui
# from nicegui.elements.label import Label

# 1. ข้อมูลอาหารเริ่มต้น
rows: list[dict[str, Any]] = [
    {"id": "01", "name": "Burger", "price": 40, "quantity": 0},
    {"id": "02", "name": "Sanwish", "price": 30, "quantity": 0},
    {"id": "03", "name": "Fired", "price": 20, "quantity": 0},
    {"id": "04", "name": "Coke", "price": 10, "quantity": 0},
]


# 2. ฟังก์ชันอัปเดตสรุปยอดสั่งซื้อด้านล่าง
def update_ui_display() -> None:
    total_bill: int = sum(row["price"] * row["quantity"] for row in rows)
    # แก้ไขจุด row[['name']] ให้เป็น row['name'] ปกติ
    ordered_items: list[str] = [
        f"{row['name']} : {row['price']}x{row['quantity']} = {row['price'] * row['quantity']}"
        for row in rows
        if row["quantity"] > 0
    ]

    # เปลี่ยนชื่อตัวแปรให้ตรงกับป้ายสรุปด้านล่าง
    if ordered_items:
        summary_text.set_text(
            f"🛒 food ordered: {', '.join(ordered_items)} | Total bill: {total_bill}฿"
        )
    else:
        summary_text.set_text("❌ not yet selected")


# 3. ฟังก์ชันควบคุมปุ่ม เพิ่ม/ลด จำนวน (เพิ่มพารามิเตอร์ total_element เข้ามา)
def change_qty(
    item: dict[str, Any], amount: int, label_element: ui.label, total_element: ui.label
) -> None:
    item["quantity"] = max(0, item["quantity"] + amount)
    label_element.set_text(str(item["quantity"]))
    total_element.set_text(f"{item['price'] * item['quantity']} ฿")

    update_ui_display()


# --- ส่วนจัดวางหน้าจอ Web UI ---
ui.label("Food Order App").classes("text-2xl font-bold m-4")

with ui.grid(columns=5).classes(
    "m-4 font-bold text-center border-b items-center max-w-xl"
):
    ui.label("No").classes("text-left")
    ui.label("Name").classes("text-left")
    ui.label("Price")
    ui.label("Quantity")
    ui.label("Total")

# วนลูปแสดงสินค้า
for item in rows:
    with ui.grid(columns=5).classes(
        "m-4 text-center items-center max-w-xl border-b pb-2"
    ):
        ui.label(item["id"]).classes("text-left")
        ui.label(item["name"]).classes("text-left")
        ui.label(f"{item['price']} ฿")

        with ui.row().classes("items-center justify-center gap-2"):
            # แก้ไขชื่อตัวแปรปุ่มให้ตรงกันทั้งหมดเรียงลำดับซ้ายไปขวา
            minus_btn = ui.button(icon="remove").props("round dense color='negative'")
            qty_label = ui.label(str(item["quantity"])).classes("w-6 text-center")
            plus_btn = ui.button(icon="add").props("round dense color='positive'")

        real_total_label = ui.label("0 ฿").classes("font-semibold")

        # ผูกฟังก์ชันเข้ากับปุ่มกด โดยส่งแอตทริบิวต์เข้าไปครบ 4 ตัวแปร
        minus_btn.on_click(
            lambda e, i=item, q=qty_label, t=real_total_label: change_qty(i, -1, q, t)
        )
        plus_btn.on_click(
            lambda e, i=item, q=qty_label, t=real_total_label: change_qty(i, 1, q, t)
        )

# ประกาศตัวแปรสรุปข้อความไว้ด้านนอก เพื่อให้ฟังก์ชันข้างบนมองเห็น
summary_text = ui.label("❌ not order yet").classes(
    "m-4 text-lg text-primary font-semibold"
)


# 4. ฟังก์ชันพิมพ์บิลส่งออกทางหน้าต่าง Terminal
def checkout() -> None:
    # แก้ไขโครงสร้าง List Comprehension ให้มีคำว่า in และเงื่อนไขการเลือกสั่ง (> 0)
    receipt: list[dict[str, Any]] = [row for row in rows if row["quantity"] > 0]
    print("\n====== Receipt Order bill ======")
    for item in receipt:
        print(
            f"menu: {item['name']} | Quantity: {item['quantity']} | Sub-total: {item['price'] * item['quantity']} Baht \n"
        )
    print("================================\n")
    ui.notify("Order done! See the receipt in Terminal")


ui.button("Check out", on_click=checkout).classes("m-4")

ui.run(title="test3")
