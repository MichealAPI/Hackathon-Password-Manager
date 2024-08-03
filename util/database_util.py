import json
from cryptography.fernet import Fernet


def write_content(file_name, key, data) -> None:
    with open(file_name, "w") as file:
        f = Fernet(key)
        encrypted_data = f.encrypt(json.dumps(data).encode())

        file.write(encrypted_data.decode())


def read_content(file_name, key) -> dict:
    with open(file_name, "r") as file:
        f = Fernet(key)
        encrypted_data = file.read()

        return json.loads(f.decrypt(encrypted_data.encode()).decode())
