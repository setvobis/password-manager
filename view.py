import tkinter as tk
from tkinter import messagebox
from typing import Callable


TITLE = "Password Manager"
WIDTH = 200
HEIGHT = 200
IMG_PATH = "lock.png"


class PasswordManager(tk.Tk):
    def __init__(self, model) -> None:
        super().__init__()
        self.model = model
        self.title(TITLE)
        self.config(padx=50, pady=50)
        self.resizable(width=False, height=False)

        self.create_ui()

    def create_ui(self) -> None:
        self.canvas = tk.Canvas()
        self.canvas.config(width=WIDTH, height=HEIGHT)
        self.image = tk.PhotoImage(file=IMG_PATH)
        self.canvas.create_image(
            WIDTH / 2,
            HEIGHT / 2,
            image=self.image,
        )
        self.canvas.grid(
            column=1,
            row=0,
        )

        self.website_label = tk.Label(text="Website:")
        self.website_label.grid(column=0, row=1)

        self.website_entry = tk.Entry()
        self.website_entry.grid(column=1, row=1, sticky="EW")
        self.website_entry.focus()

        self.search_button = tk.Button(text="Search")
        self.search_button.grid(column=2, row=1, sticky="EW")

        self.username_label = tk.Label(text="Username/Email:")
        self.username_label.grid(column=0, row=2)

        self.username_entry = tk.Entry()
        self.username_entry.grid(column=1, row=2, columnspan=2, sticky="EW")

        self.password_label = tk.Label(text="Password:")
        self.password_label.grid(column=0, row=3)

        self.password_entry = tk.Entry()
        self.password_entry.grid(column=1, row=3, sticky="EW")

        self.generate_button = tk.Button(text="Generate password")
        self.generate_button.grid(column=2, row=3, sticky="EW")

        self.save_button = tk.Button(text="Save", width=36)
        self.save_button.grid(column=1, row=4, columnspan=2, sticky="EW")

        self.show_saved_sites_button = tk.Button(text="Show saved websites")
        self.show_saved_sites_button.grid(
            column=1,
            row=5,
            columnspan=3,
            sticky="EW",
        )

    def bind_search_button(self, callback: Callable) -> None:
        self.search_button.config(command=callback)

    def bind_generate_button(self, callback: Callable) -> None:
        self.generate_button.config(command=callback)

    def bind_save_button(self, callback: Callable) -> None:
        self.save_button.config(command=callback)

    def bind_show_saved_sites_button(self, callback: Callable) -> None:
        self.show_saved_sites_button.config(command=callback)

    def get_website(self) -> str:
        return self.website_entry.get().lower()

    def show_password(
        self,
        website: str,
        password: dict[str, str] | None,
    ):
        if password is None:
            messagebox.showerror(
                title="Ups",
                message="Password is not present",
            )
        else:
            messagebox.showinfo(
                title=website,
                message=f"Email: {password['email']}\n"
                f"Password: {password['password']}\n",
            )

    def show_generated_password(self, password: str) -> None:
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def get_password_data(self):
        website = self.website_entry.get().lower()
        email = self.username_entry.get()
        password = self.password_entry.get()

        if (
            len(website.strip()) == 0
            or len(email.strip()) == 0
            or len(password.strip()) == 0
        ):
            messagebox.showwarning(
                message="You forgot to fill at least one entry",
            )
        else:
            return website, email, password

    def clear_entries(self):
        self.website_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.website_entry.focus()

    def show_saved(self, saved) -> None:
        self.popup_box = tk.Toplevel()
        self.popup_box.title("Saved websites")
        self.popup_box.minsize(width=260, height=50)
        self.popup_box.resizable(width=False, height=False)

        listbox = tk.Listbox(self.popup_box, height=6)

        for index, key in enumerate(saved):
            listbox.insert(index, key)

        listbox.grid(column=1, row=0, padx=25)
        self.popup_box.mainloop()
