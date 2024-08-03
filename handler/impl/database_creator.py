from handler.operation_handler import OperationHandler
import util.cryptography_util
import util.file_util as f_util
import util.database_util as db_util
from tkinter.filedialog import asksaveasfile


class DatabaseCreator(OperationHandler):

    identifier = "DatabaseCreator"

    def __init__(self):
        super().__init__(self.identifier)

    def run(self):

        file_name = asksaveasfile(mode='w', defaultextension=".db", filetypes=[("Database files", "*.db")]).name

        f_util.create_file(file_name)

        print(f"Database file {file_name} created, generating key...")

        key = util.cryptography_util.generate_key()

        print("WARNING: Save this key in a secure location, it will be needed to access the database")
        print(f"Key generated: {key}")

        db_util.write_content(file_name, key, {'success': 'Database created'})

    def get_id(self) -> str:
        return self.identifier
