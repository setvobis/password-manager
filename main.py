from controler import Controller
from model import Model
from view import PasswordManager


def main() -> None:
    model = Model()
    view = PasswordManager(model)
    controller = Controller(
        model=model,
        view=view,
    )
    controller.run()


if __name__ == "__main__":
    main()
