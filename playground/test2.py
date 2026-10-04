from typing import Any
from nicegui import ui
# from nicegui.elements.label import Label

rows: list[dict[str, Any]] = [
    {"id": "01", "name": "Burger", "price": 40, "quantity": 0},
    {"id": "02", "name": "Sanwish", "price": 30, "quantity": 0},
    {"id": "03", "name": "Fired", "price": 20, "quantity": 0},
    {"id": "04", "name": "Coke", "price": 10, "quantity": 0},
]

def update_ui_display() -> None:
    total_bill: int = sum(row["price"] * row["quantity"] for row in rows)
    ordered_items: list[str] = [
        f"{row['name']} : {row['price']}x{row['quantity']} = {row['price'] * row['quantity']}"
                for row in rows
                if row["quantity"] > 0
    ]
    if ordered_items:
        summary_text.set_text(
            f"🛒 food ordered :{','.join(ordered_items)} | Total bill: {total_bill}฿"
        )
    else:
        summary_text.set_text("❌ not yet selected")


def change_qty(item: dict[str, Any], amount: int, label_element: ui.label) -> None:
    item["quantity"] = max(0, item["quantity"] + amount)
    label_element.set_text(str(item["quantity"]))
    total_element.set_text(f"{item['price'] * item['quantity']} ฿")

    update_ui_display()


ui.label("Food Order App").classes("text-2xl")

with ui.grid(columns=5):
    ui.label("No").classes("items-center")
    ui.label("Name").classes("text-left")
    ui.label("Price")
    ui.label("Quantity")
    ui.label("Total")

for item in rows:
    with ui.grid(columns=5):
        ui.label(item["id"])
        ui.label(item['name'])
        ui.label(f"{item['price']} ฿")

        with ui.row().classes("items-center"):
            total_item_label: Label = ui.label("0 ฿")
            minus_bth= ui.button(icon='remove').props("round dense color='negative'")
            qty_label= ui.label(str(item['quantity']))
            plus_btn=ui.button(icon="add").props("round dense color='positive'")
        real_total_label = ui.label("0 ฿")
        minus_btn.on_click(
            lambda e, i=item, q=qty_label,t=real_total_label:change_qty(i,-1,q,t)
        )
        plus_btn.on_click(
            lambda e, i=item, q=qty_label,t=real_total_label:change_qty(i,1,q,t)
        )

summary_text = ui.label("❌ not order yet")

def checkout()->None:
    receipt:list[dict[str,Any]]=[row for rows if row['quantity'] <0]
    print("\n====== Receipt Orer bill ======")
    for item in receipt:
        print(
            f"menu: {item['name']} | Quantity : {item['quantity']} Sub-tota {item['price']*item['quantity']} Baht"
        )
    print("=========================\n")
    ui.notify('Order done see the receipt in terminal')

ui.button("Check out",on_click=checkout)

ui.run(title="test2")
        

