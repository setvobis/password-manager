from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


class PasswordManager:
    def __init__(self, email: str):
        """Provided email will be used as a default one"""

        self.email = email
        # initiates window
        self.window = Tk()
        self.window.title("Password Manager")
        self.window.config(padx=50, pady=50)
        self.window.resizable(width=False, height=False)
        # decorates window
        self.canvas = Canvas()
        self.canvas.config(width=200, height=200)
        self.lock_image = PhotoImage(file="lock.png")
        self.canvas.create_image(100, 100, image=self.lock_image)
        self.canvas.grid(column=1, row=0)
        # UI setup
        # sets website name label
        self.website_label = Label(text="Website:")
        self.website_label.grid(column=0, row=1)
        # initiates website name entry
        self.website_entry = Entry()
        self.website_entry.grid(column=1, row=1, sticky="EW")
        self.website_entry.focus()
        # initiates search button
        self.search_button = Button(text="Search", command=self.find_password)
        self.search_button.grid(column=2, row=1, sticky="EW")
        # sets username/email label
        self.username_label = Label(text="Username/Email:")
        self.username_label.grid(column=0, row=2)
        # initiates username/email entry
        self.username_entry = Entry()
        self.username_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
        self.username_entry.insert(0, self.email)
        # sets password label
        self.password_label = Label(text="Password:")
        self.password_label.grid(column=0, row=3)
        # initiates password entry
        self.password_entry = Entry()
        self.password_entry.grid(column=1, row=3, sticky="EW")
        # sets 'generate password' button
        self.generate_button = Button(text="Generate password", command=self.generate_password)
        self.generate_button.grid(column=2, row=3, sticky="EW")
        # sets 'save' button
        self.save_button = Button(text="Save", width=36, command=self.save_password)
        self.save_button.grid(column=1, row=4, columnspan=2, sticky="EW")
        # sets 'show saved websites' button
        self.show_saved_sites_button = Button(text="Show saved websites", command=self.show_saved)
        self.show_saved_sites_button.grid(column=1, row=5, columnspan=3, sticky="EW")
        # prevents app from closing
        self.window.mainloop()
        self.popup_box = None

    def find_password(self):
        website = self.website_entry.get().lower()
        try:
            # `homework` ;)
            with open("homework.json") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showerror(title="Ups", message="No Data File Found")
        else:
            try:
                messagebox.showinfo(title=website, message=f"Email: {data[website]['email']}\n"
                                                           f"Password: {data[website]['password']}\n"
                                                           "Password copied to clipboard")
                pyperclip.copy(data[website]["password"])
            except KeyError:
                messagebox.showerror(title=website, message="No details for the website exists")

    def generate_password(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u',
                   'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                   'P',
                   'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        password_letters = [choice(letters) for _ in range(randint(8, 10))]
        password_numbers = [choice(numbers) for _ in range(randint(3, 5))]
        password_symbols = [choice(symbols) for _ in range(randint(3, 5))]

        password_list = password_letters + password_numbers + password_symbols
        shuffle(password_list)

        password = "".join(password_list)

        self.password_entry.delete(0, END)
        self.password_entry.insert(0, password)
        pyperclip.copy(password)

    def save_password(self):
        website = self.website_entry.get().lower()
        email = self.username_entry.get()
        password = self.password_entry.get()

        # data is stored in JSON format
        new_data = {
            website: {"email": email,
                      "password": password
                      }
        }

        # checking if all entries are filled
        if len(website.strip()) == 0 or len(email.strip()) == 0 or len(password.strip()) == 0:
            messagebox.showwarning(message="You forgot to fill at least one entry")
        else:
            is_ok = messagebox.askokcancel(title=website, message=f"Email/username: {email}\n"
                                                                  f"Password: {password}\nIs it okay?")
            if is_ok:

                try:
                    with open("homework.json", mode="r") as data_file:
                        # reading old data
                        data = json.load(data_file)
                except FileNotFoundError:
                    with open("homework.json", "w") as data_file:
                        json.dump(new_data, data_file, indent=4)
                else:
                    # updating
                    data.update(new_data)
                    with open("homework.json", mode="w") as data_file:
                        # saving updated
                        json.dump(data, data_file, indent=4)
                finally:
                    self.website_entry.delete(0, END)
                    self.password_entry.delete(0, END)
                    self.website_entry.focus()

    def show_saved(self):
        # initiates new, top level window
        self.popup_box = Toplevel()
        self.popup_box.title("Saved websites")
        self.popup_box.minsize(width=260, height=50)
        self.popup_box.resizable(width=False, height=False)

        # another image, purely visual reason
        second_canvas = Canvas(self.popup_box)
        second_canvas.config(width=200, height=200)
        second_canvas.create_image(100, 100, image=self.lock_image)
        second_canvas.grid(column=0, row=0)
        # list of websites with data provided by user
        listbox = Listbox(self.popup_box, height=6)
        with open("homework.json") as data_file:
            data = json.load(data_file)

        key_list = list(data.keys())
        for key in key_list:
            listbox.insert(key_list.index(key), key)

        listbox.grid(column=1, row=0, padx=25)

        self.popup_box.mainloop()


if __name__ == '__main__':
    pm = PasswordManager("test@mail.com")
