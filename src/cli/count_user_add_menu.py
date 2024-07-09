from typing import Union, Any, List

from src.db_use.save_user import save_user
from src.json_parsing import get_users_url, pars_user
from src.json_parsing.model.users import Users
from src.settings import Settings


def count_user_add_menu(settings: Settings) -> bool:
    """
    Корректно передаеет вводимые данные для добавления пользователя
    :param settings: Данные для подключения к бд
    :return: Ture - если пользователь успешно добавлен,
    False - если не удалось добавить пользователя
    """
    while True:
        try:
            count_user: int = int(input("введите количество пользователей: "))
            json_result: Union[list[dict[Any, Any]], bool] = get_users_url(
                count_user, settings
            )
            if isinstance(json_result, list):
                users_result: Union[List[Users], bool] = pars_user(json_result)
                if isinstance(users_result, list):
                    for user in users_result:
                        if not save_user(settings, user):
                            print("Не получилось добавить пользователя")
                            return False
                        else:
                            print("Пользователь успешно добавлен")
                return True
            else:
                print("Не удалось получить данные")
                return False
        except TypeError:
            return False
        except ValueError:
            print("введите число")
