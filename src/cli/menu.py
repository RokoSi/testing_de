import sys
from typing import Callable, List, Union, Dict, Any, Optional

from src.db_use import get_users_db, get_check_email
from src.json_parsing.model.users import Users
from src.settings import Settings
from src.db_use.data_provider import (
    create_db,
)

from src.db_use.save_user import save_user
from src.db_use.user_update import (
    update_param_table_contact_details_db,
    update_param_table_media_data_db,
    update_param_table_registration_data_db,
    update_param_table_users_db,
    del_user,
    update_param_table_cities_db,
    update_param_table_locations_db,
)
from src.json_parsing.get_user import get_users_url
from src.json_parsing.pars import pars_user
from src.validators.validator_email import validator_email


def main_menu(settings: Settings):
    """
    Cli для взаимодействия с функционалом.
    :param settings: Данные для подключения к бд.
    """
    menu_elements: List[str] = [
        "1. Добавить пользователей",
        "2. Получить валидных пользователей",
        "3. Получить невалидных пользователей",
        "4. Проверить наличие email",
        "5. Изменение данных",
        "6. Удалить пользователя",
        "7. Выйти",
    ]

    create_db(settings)

    choices_part_func: Dict[int, Callable] = {
        1: count_user_add_menu,
        2: valid_users,
        3: invalid_users,
        4: check_email,
        5: update_param,
        6: delite_user,
        7: exit_program,
    }

    while True:
        print("Меню:")
        for item in menu_elements:
            print(item)
        try:
            choice: int = int(input("Выберите пункт меню: "))
            if choice in choices_part_func:
                action_menu = choices_part_func[choice]
                if choice != 7:
                    action_menu(settings)
                else:
                    action_menu()
            else:
                print("Выбранная опция не поддерживается")
        except ValueError:
            print("введите число")


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


def valid_users(settings: Settings) -> bool:
    """
    Получение валидных пользователей и их вывод
    :param settings: Данные для подключения к бд
    :return: Ture - если удалось найти таких пользователй,
    False - если не удалось найти таких пользователей
    """
    results: Union[List[Dict], bool] = get_users_db(settings, True)
    if isinstance(results, list):
        if results:
            for row in results:
                print(", ".join(map(str, row)))
            return True
        else:
            print("нет таких записей\n")
            return False
    else:
        print("Ошибка при получении данных")
        return False


def invalid_users(settings: Settings) -> bool:
    """
    Получение не валидных пользователей и их вывод
    :param settings: Данные для подключения к бд
    :return: Ture - если удалось найти таких пользователй,
     False - если не удалось найти таких пользователей
    """
    results: Union[List[Dict], bool] = get_users_db(settings, False)
    if isinstance(results, list):
        if results:
            for row in results:
                print(", ".join(map(str, row)))
            return True
        else:
            print("нет таких записей")
            return False
    else:
        print("Ошибка при получении данных")
        return False


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


def update_param(settings: Settings) -> bool:
    """
    Изменение параметров
    :param settings: Данные для подключения к бд
    :return: Ture - если данные успешно изменены, False - если ошибка изменения данных
    """
    update_attr: Dict[str, List[str]] = {
        "city": ["cities"],
        "state": ["cities"],
        "country": ["cities"],
        "phone": ["contact_details"],
        "cell": ["contact_details"],
        "street_name": ["locations"],
        "street_number": ["locations"],
        "postcode": ["locations"],
        "latitude": ["locations"],
        "longitude": ["locations"],
        "picture": ["media_data"],
        "email": ["registration_data"],
        "username": ["registration_data"],
        "password": ["registration_data"],
        "password_md5": ["registration_data"],
        "gender": ["users"],
        "name_title": ["users"],
        "name_first": ["users"],
        "name_last": ["users"],
        "age": ["users"],
        "nat": ["users"],
    }
    print(
        *[f"{i}. {key}" for i, key in enumerate(update_attr.keys(), start=1)], sep="\n"
    )
    try:
        num_param: int = int(input("выберите параметр на изменение:"))
        options: List[str] = list(update_attr.keys())

        if num_param < 1 or num_param > len(options):
            raise IndexError(
                "Выбранный номер параметра выходит за пределы допустимого диапазона"
            )

        selected_key: str = options[int(num_param) - 1]
        print("Вы выбрали параметр:", selected_key)

        value: Union[str, int] = input("На что поменять: ")
        email_user: str = input("Выберете пользователя по email: ")
        select_table: Optional[List[str]] = update_attr.get(selected_key)

        if select_table is None:
            print("Не удалось найти таблицу для обновления")
            return False

        update_functions: Dict[str, Callable] = {
            "cities": update_param_table_cities_db,
            "contact_details": update_param_table_contact_details_db,
            "locations": update_param_table_locations_db,
            "media_data": update_param_table_media_data_db,
            "registration_data": update_param_table_registration_data_db,
            "users": update_param_table_users_db,
        }

        if select_table[0] in update_functions:
            if update_functions[select_table[0]](
                settings, email_user, selected_key, value
            ):
                print("успешно")
                return True
            else:
                print("не успешно")
                return False
        return False
    except (ValueError, IndexError):
        print("Некорректный ввод. Пожалуйста, введите число от 1 до", len(update_attr))
        return False


def delite_user(settings: Settings) -> None:
    """
    Удаление пользователя по email, если он валиден
    :param settings: Данные для подключения к бд
    """
    while True:
        email: str = str(input("введите email: "))
        if validator_email(email):
            check_del: bool = del_user(settings, email)
            if check_del:
                print("Пользовать удален\n")
                break
            else:
                print("Нет такого пользователя")
                break
        else:
            print("введите валидный пароль")


def exit_program() -> None:
    """
    Метод для завершения программы
    """
    sys.exit()


if __name__ == "__main__":
    pass