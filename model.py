import string
import random
import json

ASCII_NUMBER = 8
DIGITS_NUMBER = 4
SYMBOLS_NUMBER = 4
DB_FILENAME = "homework.json"


class Model:
    def __init__(self) -> None:
        try:
            with open(DB_FILENAME, "r") as f:
                data = json.load(f)
                if data is None:
                    data = {}
                self.data = data
        except FileNotFoundError:
            with open(DB_FILENAME, "w") as f:
                json.dump({}, f, indent=4)
                self.data = {}

    def generate_password(self) -> str:
        letters = [random.choice(string.ascii_letters) for _ in range(ASCII_NUMBER)]
        numbers = [random.choice(string.digits) for _ in range(DIGITS_NUMBER)]
        symbols = [random.choice("!#$%&()*+") for _ in range(SYMBOLS_NUMBER)]

        password_list = letters + numbers + symbols
        random.shuffle(password_list)
        return "".join(password_list)

    def find_password(self, website) -> dict[str, str] | None:
        return self.data.get(website)

    def save_password(self, website, email, password):
        new_data = {
            website: {
                "email": email,
                "password": password,
            }
        }

        self.data.update(new_data)
        with open(DB_FILENAME, mode="w") as f:
            json.dump(self.data, f, indent=4)

    def show_saved(self):
        return self.data.keys()
