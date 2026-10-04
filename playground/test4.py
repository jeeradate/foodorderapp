from typing import Any, Dict, List
from nicegui import ui

# --------------------------------------------------
# Mock Data: สมมุติว่าเป็นข้อมูลรายการอาหารจาก Database
# --------------------------------------------------
food_items: List[Dict[str, Any]] = [
    {"id": 1, "name": "Pad Thai", "price": 80, "category": "Noodles"},
    {"id": 2, "name": "Tom Yum Goong", "price": 150, "category": "Soup"},
    {"id": 3, "name": "Green Curry", "price": 120, "category": "Curry"},
    {"id": 4, "name": "Fried Rice", "price": 70, "category": "Rice"},
]


# ==================================================
# 1. ตัวอย่างการใช้ ui.grid (สร้าง Food Card Layout)
# ==================================================
def render_food_grid(items: List[Dict[str, Any]]) -> None:
    ui.label("1. Example of ui.grid (Food Cards)").classes("text-h6 mt-4")

    # กำหนด columns=3 เพื่อให้แสดงผล 3 คอลัมน์
    with ui.grid(columns=3).classes("w-full gap-4"):
        for item in items:
            # ใน grid เราสามารถใส่ UI Element อะไรก็ได้ เช่น ui.card
            with ui.card().classes("p-4 border shadow-sm"):
                ui.label(item["name"]).classes("font-bold text-lg")
                ui.label(f"Category: {item['category']}").classes("text-gray-500")
                ui.label(f"Price: ฿{item['price']}").classes(
                    "text-green-600 font-semibold"
                )

                # เพิ่มปุ่มกดสั่งอาหารเข้า Cart
                ui.button(
                    "Add to Cart",
                    on_click=lambda i=item: ui.notify(f"Added {i['name']}"),
                ).props("small color=primary")


# ==================================================
# 2. ตัวอย่างการใช้ ui.table (สร้าง Order/Menu Table)
# ==================================================
def render_food_table(items: List[Dict[str, Any]]) -> None:
    ui.label("2. Example of ui.table (Data Table)").classes("text-h6 mt-4")

    # กำหนดโครงสร้างคอลัมน์ของ Table
    columns: List[Dict[str, Any]] = [
        {
            "name": "id",
            "label": "ID",
            "field": "id",
            "required": True,
            "sortable": True,
        },
        {
            "name": "name",
            "label": "Menu Name",
            "field": "name",
            "sortable": True,
        },
        {"name": "category", "label": "Category", "field": "category"},
        {
            "name": "price",
            "label": "Price (THB)",
            "field": "price",
            "sortable": True,
        },
    ]

    # สร้าง Table โดยส่ง columns และ rows เข้าไปตรงๆ
    ui.table(columns=columns, rows=items, row_key="id").classes("w-full")


# --------------------------------------------------
# Main Execution Layout
# --------------------------------------------------
render_food_grid(food_items)
ui.separator()
render_food_table(food_items)

ui.run(title="Grid vs Table Demo")
