import database_utils as db_utils


def print_input_menu():
    print("0. Create new Password database")
    print("1. Load Password database")

    choice = input(input("Enter your choice:\n"))

    if choice == "0":
        db_utils.handle_database_creation()

    elif choice == "1":
        content = db_utils.load_database()
        content = content + " DOES THIS WORK?"
        db_utils.save_database(content)
