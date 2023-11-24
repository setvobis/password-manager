from model import Model
from view import PasswordManager


class Controller:
    def __init__(
        self,
        model: Model,
        view: PasswordManager,
    ) -> None:
        self.model = model
        self.view = view

        self.view.bind_search_button(self.find_password)
        self.view.bind_generate_button(self.generate_password)
        self.view.bind_save_button(self.save_password)
        self.view.bind_show_saved_sites_button(self.show_saved)

    def find_password(self) -> None:
        website = self.view.get_website()
        password = self.model.find_password(website)
        self.view.show_password(website, password)

    def generate_password(self) -> None:
        password = self.model.generate_password()
        self.view.show_generated_password(password)

    def save_password(self) -> None:
        website, email, password = self.view.get_password_data()  # type: ignore
        self.model.save_password(website, email, password)
        self.view.clear_entries()

    def show_saved(self) -> None:
        saved = self.model.show_saved()
        self.view.show_saved(saved)

    def run(self) -> None:
        self.view.mainloop()
