from nicegui import ui


@ui.page("/login")
def login_page():
    ui.label("Welcome to Login Form!")


@ui.page("/signup")
def signup_page():
    ui.label("Welcome to Signup Form!")


ui.link("Visit Login Form", login_page)
ui.link("Visit Signup Form", signup_page)

ui.run()
