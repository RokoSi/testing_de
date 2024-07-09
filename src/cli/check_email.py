from src.db_use import get_check_email
from src.settings import Settings
from src.validators import validator_email


def check_email(settings: Settings) -> None:
    """
    Если ли пользователь в бд
    :param settings: Данные для подключения к бд
    """
    while True:
        email: str = str(input("введите email: "))
        if validator_email(email):
            if get_check_email(settings, email):
                print("Пользователь есть в бд \n")
                break
            else:
                print("нет пользователя в бд")
                break
        else:
            print("введите валидный пароль")
