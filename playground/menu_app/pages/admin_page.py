from typing import Any
from nicegui import ui
from services.food_service import (
    add_category,
    add_food_item_with_options,
    get_category_options,
)


@ui.page("/admin")
def admin() -> None:
    """หน้า Admin สำหรับบริหารจัดการ Category และรายการอาหารพร้อม Options"""

    # ตัวแปรเก็บ reference ของ Input ในแต่ละแถว Option เพื่อดึงค่าไปบันทึก
    option_input_rows: list[tuple[ui.input, ui.number, ui.row]] = []

    with ui.column().classes("w-full max-w-2xl mx-auto p-6"):
        # Header
        with ui.row().classes("w-full items-center justify-between"):
            ui.label("Admin menu management").classes("text-h4")
            ui.button(
                "Back Home",
                icon="home",
                on_click=lambda: ui.navigate.to("/"),
            ).props("flat")

        # ------------------------------------------------------------------
        # ส่วนที่ 1: การเพิ่ม Category ใหม่
        # ------------------------------------------------------------------
        with ui.card().classes("w-full"):
            ui.label("Add category").classes("text-h6")
            category_name_input = ui.input(
                label="Category name:",
                placeholder="ex: One-dish, Drink",
            ).classes("w-full")

            def save_category() -> None:
                name: str = (category_name_input.value or "").strip()
                if not name:
                    ui.notify("Fill in Category", type="warning")
                    return

                add_category(name)
                category_name_input.value = ""

                # อัปเดตตัวเลือกใน Dropdown ทันที
                category_select.options = get_category_options()
                category_select.update()

                ui.notify(f"Done add category: {name}", type="positive")

            ui.button(
                "Add Category",
                icon="add",
                on_click=save_category,
            ).props("color=primary")

        # ------------------------------------------------------------------
        # ส่วนที่ 2: การเพิ่ม Food Item พร้อม Options
        # ------------------------------------------------------------------
        with ui.card().classes("w-full"):
            ui.label("Add food menu with Options").classes("text-h6")

            food_name_input = ui.input(
                label="Food name:",
                placeholder="Ex: Burger",
            ).classes("w-full")

            food_price_input = ui.number(
                label="Price (baht)",
                min=0,
                format="%.2f",
            ).classes("w-full")

            category_select = ui.select(
                options=get_category_options(),
                label="Category",
            ).classes("w-full")

            ui.separator().classes("my-2")

            # ส่วนการจัดการ Options แบบ Dynamic
            ui.label("Food Options (Optional)").classes("text-subtitle1 font-bold")
            options_container = ui.column().classes("w-full")

            def add_option_row() -> None:
                """สร้างแถวรับข้อมูล Option ใหม่"""
                with options_container:
                    with ui.row().classes("w-full items-center gap-2") as row:
                        opt_name = ui.input(
                            label="Option Name",
                            placeholder="ex: Extra Egg, No Spicy",
                        ).classes("col-6")

                        opt_price = ui.number(
                            label="Extra Price (0 = Free)",
                            value=0.0,
                            min=0,
                            format="%.2f",
                        ).classes("col-4")

                        def remove_this_row(
                            target_row: ui.row = row,
                            n_input: ui.input = opt_name,
                            p_input: ui.number = opt_price,
                        ) -> None:
                            options_container.remove(target_row)
                            option_input_rows.remove((n_input, p_input, target_row))

                        ui.button(
                            icon="delete",
                            on_click=remove_this_row,
                        ).props("flat color=negative").classes("mt-2")

                        option_input_rows.append((opt_name, opt_price, row))

            ui.button(
                "Add Option Row",
                icon="add_circle_outline",
                on_click=add_option_row,
            ).props("flat color=secondary")

            ui.separator().classes("my-4")

            def save_food_item() -> None:
                name: str = (food_name_input.value or "").strip()
                price: float | None = food_price_input.value
                category_id: Any = category_select.value

                if not name:
                    ui.notify("Input food name", type="warning")
                    return
                if price is None or price < 0:
                    ui.notify("Input food price", type="warning")
                    return
                if not category_id:
                    ui.notify("Select Category", type="warning")
                    return

                # รวบรวมข้อมูล Options จาก UI
                options_data: list[dict[str, str | float]] = []
                for name_input, price_input, _ in option_input_rows:
                    o_name: str = (name_input.value or "").strip()
                    o_price: float = (
                        price_input.value if price_input.value is not None else 0.0
                    )
                    if o_name:
                        options_data.append({"name": o_name, "extra_price": o_price})

                # บันทึกลง Database
                add_food_item_with_options(
                    name=name,
                    price=float(price),
                    category_id=int(category_id),
                    options_data=options_data,
                )

                # Reset ฟอร์มหลังบันทึก
                food_name_input.value = ""
                food_price_input.value = None
                category_select.value = None
                options_container.clear()
                option_input_rows.clear()

                ui.notify(f"Menu: {name} added successfully!", type="positive")

            ui.button(
                "Save Food Item",
                icon="save",
                on_click=save_food_item,
            ).props("color=primary").classes("w-full mt-2")

            ui.separator().classes("my-2")

            ui.button(
                "See the menu",
                icon="menu_book",
                on_click=lambda: ui.navigate.to("/menu"),
            ).props("outline").classes("w-full")
