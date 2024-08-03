from handler.operation_handler import OperationHandler


def handle_menu(handlers: dict):  # dict: {description: OperationHandler}

    while True:
        operations = print_menu(handlers)
        choice = int(input("Enter the number of the operation you want to perform:\n"))

        if choice < 0 or choice >= len(operations):
            print("Invalid choice, please try again")
            continue

        val = operations[choice].run()

        if operations[choice].get_id() == "DatabaseLoader" and val is not None:
            print(val)
            break


def print_menu(handlers: dict) -> list:
    """
    Print the menu and return the indexed operations
    :param handlers: operation handlers
    :return: indexed operations
    """
    operations = []
    counter = 0

    for description, handler in handlers.items():
        print(f"{counter}. {description}")

        operations.append(handler)
        counter += 1

    return operations
