from nicegui import ui


class CounterController:
    """Controller สำหรับจัดการ Business Logic และ State"""

    def __init__(self) -> None:
        self.value: int = 0

    def increment(self) -> int:
        self.value += 1
        return self.value

    def reset(self) -> int:
        self.value = 0
        return self.value


def create_ui(controller: CounterController) -> None:
    """Function สำหรับสร้าง UI แยกจาก Logic"""
    ui.label("Separated Pattern Example").classes("text-xl font-bold")

    label = ui.label(f"Count: {controller.value}").classes("text-lg")

    def on_click_increment() -> None:
        new_val = controller.increment()
        label.set_text(f"Count: {new_val}")

    def on_click_reset() -> None:
        new_val = controller.reset()
        label.set_text(f"Count: {new_val}")

    with ui.row():
        ui.button("Increment", on_click=on_click_increment).props("color=green")
        ui.button("Reset", on_click=on_click_reset).props("color=red")


controller = CounterController()
create_ui(controller)

ui.run()
