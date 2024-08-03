import json
import tkinter

from app.password_manager_app import PasswordManagerApp
from handler.operation_handler import OperationHandler
import util.cryptography_util
import util.file_util as f_util
from tkinter.filedialog import askopenfilename
from tkinter import *
from tkinter import messagebox


class DatabaseLoader(OperationHandler):

    identifier = "DatabaseLoader"

    def __init__(self):
        super().__init__(self.identifier)

    def run(self):

        key = bytes(input("Enter the key to decrypt the database with:\n"), "utf-8")

        print("Select the database file to load...")

        file_name = askopenfilename(filetypes=[("Database files", "*.db")])

        if not f_util.exists(file_name):
            print(f"Database file {file_name} does not exist")
            return

        print(f"Reading database file {file_name}...")

        encrypted_content = f_util.read_file(file_name)

        print("Decrypting database...")

        f = util.cryptography_util.Fernet(key)

        decrypted_content = f.decrypt(encrypted_content)

        val = json.loads(decrypted_content.decode("utf-8"))

        if val is not None:
            root = tkinter.Tk()

            PasswordManagerApp(root, "default_key", file_name, key)

            root.mainloop()

    def get_id(self) -> str:
        return self.identifier


