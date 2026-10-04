from nicegui import ui
from sqlmodel import SQLModel
from database import engine, save_user_to_db, get_all_users_from_db

SQLModel.metadata.create_all(engine)


def handle_save(username_input, email_input, refreshable_target):
    if not username_input.value or not email_input.value:
        ui.notify("Please fill in all fields!", type="warning")
        return
    save_user_to_db(username_input.value, email_input.value)

    username_input.value = ""
    email_input.value = ""
    ui.notify("User saved successfully!", type="positive")
    refreshable_target.refresh()


@ui.refreshable
def user_table():
    users = get_all_users_from_db()
    columns = [
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "username", "label": "username", "field": "username"},
        {"name": "email", "label": "Email", "field": "email"},
    ]
    ui.table(columns=columns, rows=[user.model_dump() for user in users], row_key="id")


@ui.page("/")
def main_apge():
    ui.label("User Management System").classes("text-h4")
    with ui.card():
        ui.label("Add New User")
        username = ui.input(label="User name: ")
        email = ui.input(label="Email : ")

        table_box = ui.element("div")
        with table_box:
            user_table()

        ui.button(
            "Save user", on_click=lambda: handle_save(username, email, user_table)
        )


if __name__ in {"__main__", "__mp_main__", "<run_path>"}:
    ui.run(title="Register")
