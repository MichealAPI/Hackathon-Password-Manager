from cryptography.fernet import Fernet


def load_database() -> str:
    file_name: str = input("Enter the name of the file:\n")

    try:
        with open(file_name, "rb") as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f"Database {file_name} not found")

    try:
        with open("key.key", "rb") as key_file:
            key = key_file.read()
            print("Key found")
    except FileNotFoundError:
        print("Key not found")

    f = Fernet(key)

    file_content = f.decrypt(file_content)

    return file_content.decode("utf-8")


def save_database(file_content: str):
    file_name: str = input("Enter the name of the file:\n")

    try:
        with open("key.key", "rb") as key_file:
            key = key_file.read()
            print("Key found")
    except FileNotFoundError:
        print("Key not found")

    f = Fernet(key)

    file_content = f.encrypt(file_content.encode("utf-8"))

    with open(file_name, "wb") as file:
        file.write(file_content)

    print(f"Database {file_name} saved successfully")


def handle_database_creation():
    file_name: str = input("Enter the name of the file:\n")

    with open(file_name, "w") as file:
        file.write("")

    print(f"Database {file_name} created successfully")

    write_key()

    print("Key generated successfully")


def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)