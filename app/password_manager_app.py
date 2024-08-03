import os
import tkinter as tk
from tkinter import messagebox

import util.database_util as db_utils  # Ensure this matches your actual file structure


class PasswordManagerApp:

    def __init__(self, root, key: str, file_name: str, encryption_key: bytes):
        self.root = root
        self.root.title("Simple Password Manager")
        self.is_password_visible = False

        self.file_name = file_name

        # Initialize entries list
        self.entries = []

        # Key for loading specific entries
        self.key = key

        # Encryption key (You should store this securely)
        self.encryption_key = encryption_key  # Replace with your actual key

        # Create widgets
        self.create_widgets()

        # Load entries from file
        self.load_entries_from_file()


    def create_widgets(self):
        # Service Name
        tk.Label(self.root, text="Service Name").grid(row=0, column=0, padx=10, pady=5)
        self.service_name_entry = tk.Entry(self.root)
        self.service_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Username
        tk.Label(self.root, text="Username").grid(row=1, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        # Password
        tk.Label(self.root, text="Password").grid(row=2, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Buttons
        self.create_button = tk.Button(self.root, text="Create", command=self.create_entry)
        self.create_button.grid(row=3, column=0, padx=10, pady=5)

        self.save_button = tk.Button(self.root, text="Save", command=self.save_entry)
        self.save_button.grid(row=3, column=1, padx=10, pady=5)

        self.edit_button = tk.Button(self.root, text="Edit", command=self.edit_entry)
        self.edit_button.grid(row=4, column=0, padx=10, pady=5)

        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_entry)
        self.delete_button.grid(row=4, column=1, padx=10, pady=5)

        self.show_button = tk.Button(self.root, text="Show", command=self.show_pwd)
        self.show_button.grid(row=2, column=2, padx=10, pady=5)

        # Listbox to display entries
        self.entries_listbox = tk.Listbox(self.root)
        self.entries_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        self.entries_listbox.bind('<<ListboxSelect>>', self.on_entry_select)

    def create_entry(self):
        service_name = self.service_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not service_name or not username or not password:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        entry = {"service_name": service_name, "username": username, "password": password}
        self.entries.append(entry)
        self.update_entries_listbox()
        self.save_entries_to_file()

    def save_entry(self):
        selected_index = self.entries_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No entry selected")
            return

        service_name = self.service_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not service_name or not username or not password:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        entry = {"service_name": service_name, "username": username, "password": password}
        self.entries[selected_index[0]] = entry
        self.update_entries_listbox()
        self.save_entries_to_file()

    def show_pwd(self):

        selected_index = self.entries_listbox.curselection()
        if selected_index and not self.is_password_visible:
            self.password_entry = tk.Entry(self.root)
            self.password_entry.grid(row=2, column=1, padx=10, pady=5)
            self.password_entry.insert(0, self.entries[selected_index[0]]["password"])


        elif selected_index and self.is_password_visible:
            self.password_entry = tk.Entry(self.root, show="*")
            self.password_entry.grid(row=2, column=1, padx=10, pady=5)
            self.password_entry.insert(0, self.entries[selected_index[0]]["password"])

        self.is_password_visible = not self.is_password_visible

    def edit_entry(self):
        selected_index = self.entries_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No entry selected")
            return

        entry = self.entries[selected_index[0]]
        self.service_name_entry.delete(0, tk.END)
        self.service_name_entry.insert(0, entry["service_name"])
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, entry["username"])
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, entry["password"])

    def delete_entry(self):
        selected_index = self.entries_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No entry selected")
            return

        del self.entries[selected_index[0]]
        self.update_entries_listbox()
        self.save_entries_to_file()

    def on_entry_select(self, event):
        selected_index = self.entries_listbox.curselection()
        if selected_index:
            entry = self.entries[selected_index[0]]
            self.service_name_entry.delete(0, tk.END)
            self.service_name_entry.insert(0, entry["service_name"])
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, entry["username"])
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, entry["password"])

    def update_entries_listbox(self):
        self.entries_listbox.delete(0, tk.END)
        for entry in self.entries:
            self.entries_listbox.insert(tk.END, f"{entry['service_name']} - {entry['username']}")

    def load_entries_from_file(self):
        if os.path.exists(self.file_name):
            try:
                data = db_utils.read_content(self.file_name, self.encryption_key)
                if self.key in data:
                    self.entries = data[self.key]
                    self.update_entries_listbox()
                else:
                    messagebox.showwarning("Load Error", f"No entries found for key: {self.key}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load entries: {e}")

    def save_entries_to_file(self):
        data = {}
        if os.path.exists(self.file_name):
            try:
                data = db_utils.read_content(self.file_name, self.encryption_key)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read existing entries: {e}")

        data[self.key] = self.entries

        try:
            db_utils.write_content(self.file_name, self.encryption_key, data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save entries: {e}")
