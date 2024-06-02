import logging
import sys

from model.Settings import Settings
from src.DataProvider.DataProviderDB import update_param_table_cities_db, update_param_table_contact_details_db, \
    update_param_table_locations_db, update_param_table_media_data_db, update_param_table_registration_data_db, \
    update_param_table_users_db, get_check_email, get_users_db
from src.DataProvider.DataProviderURl import get_users_url,  parsing_and_save_file
from resources.constants import update_attr

log = logging.getLogger(__name__)
settings: Settings = Settings()


def add_users() -> bool:
    """
    Метод для ввода количества пользователей,вызов парсера
    :return: возвращает True - если запрос выполнен без ошибок,False - если ошибка введенного значения
    """
    count_user_in_db: int = 0
    exit_add: bool = True
    while exit_add:
        try:
            count: int = int(input("введите количество пользователей: "))
            if count:
                json_file: [dict | bool] = get_users_url(count)
                if json_file:
                    count_user_in_db: int = parsing_and_save_file(json_file)
                else:
                    print("Не удалось добавить запись")
            print("Успешно добавлено: ", count_user_in_db, "записей")
            exit_add = False
            return True
        except ValueError:
            print("ОШИБКА: ведите число:  ")
    return False


def get_invalid_users() -> bool:
    """
        Метод для вывод не валидных пользователей
        :return: True - если есть такие пользователи, False - если нет
        """
    results = get_users_db(False)
    if results:
        for row in results:
            print(", ".join(map(str, row)))
        return True
    else:
        print("нет таких записей")
        return False


def get_valid_users():
    """
        Метод для вывода валидных пользователей
        :return: True - если есть такие пользователи, False - если нет
        """
    results = get_users_db(True)
    if results:
        for row in results:
            print(", ".join(map(str, row)))
        return True
    else:
        print("нет таких записей\n")
        return False


def email_check() -> bool:
    """
        Метод для обработки результата проверки email в бд
        :return: True - если есть такой пользователь, False - если нет
        """
    email: str = input("введите email:")
    answer_email: [dict | bool] = get_check_email(email)
    if answer_email:
        print(f"есть такой email в базе\n ")
        return True

    else:
        print("нет такого email в базе\n")
        return False


def update_param() -> bool:
    """
    Метод для выбора пользователя, какой парамент поменять, на какое значение и кому
    :return: True - если метод на выполнения есть, False - если нет или если не корректный ввод
    """
    print(*[f"{i}. {key}" for i, key in enumerate(update_attr.keys(), start=1)], sep='\n')
    num_param = input("выберите параметр на изменение:")
    options = list(update_attr.keys())
    try:

        selected_key = options[int(num_param) - 1]
        print("Вы выбрали параметр:", selected_key)

        value = input("На что поменять: ")
        email_user = input("Выберете пользователя по email: ")

        select_table = update_attr.get(selected_key)

        update_functions = {
            'cities': update_param_table_cities_db,
            'contact_details': update_param_table_contact_details_db,
            'locations': update_param_table_locations_db,
            'media_data': update_param_table_media_data_db,
            'registration_data': update_param_table_registration_data_db,
            'users': update_param_table_users_db
        }

        if select_table[0] in update_functions:
            update_functions[select_table[0]](email_user, selected_key, value)
            return True
    except (ValueError, IndexError):
        print("Некорректный ввод. Пожалуйста, введите число от 1 до", len(options))
        return False


def exit_program():
    """
    Метод для завершения программы
    """
    sys.exit()
