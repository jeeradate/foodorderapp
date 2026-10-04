from nicegui import ui
from database import create_db_and_tables
import pages.home_page  # noqa: F401
import pages.menu_page  # noqa: F401
import pages.admin_page  # noqa:F401

create_db_and_tables()


ui.run(title="Menu app 2", reload=True)
