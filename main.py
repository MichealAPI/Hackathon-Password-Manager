from handler.impl.database_loader import DatabaseLoader
from handler.impl.database_creator import DatabaseCreator
from menu_handler import handle_menu

handlers = {
    "Loads a Database from file": DatabaseLoader(),
    "Creates a new Database file along with its encryption key": DatabaseCreator()
}

handle_menu(handlers)
