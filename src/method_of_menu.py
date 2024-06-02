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


def get_invalid_users():
    results = get_users_db(False)
    if results:
        for row in results:
            print(", ".join(map(str, row)))
    else:
        print("нет таких записей")


def get_valid_users():
    results = get_users_db(True)
    if results:
        for row in results:
            print(", ".join(map(str, row)))
    else:
        print("нет таких записей\n")


def email_check():
    email: str = input("введите email:")
    answer_email: [list | bool] = get_check_email(email)
    if answer_email:
        print("есть такой email в базе\n")

    else:
        print("нет такого email в базе\n")


def update_param():
    print(*[f"{i}. {key}" for i, key in enumerate(update_attr.keys(), start=1)], sep='\n')
    num_param = input("выберите параметр на изменение:")
    try:
        options = list(update_attr.keys())
        selected_key = options[int(num_param) - 1]
        print("Вы выбрали параметр:", selected_key)

        value = input("На что поменять: ")
        email_user = input("Выберете пользователя по email: ")

        select_table = update_attr.get(selected_key)
        print(select_table[0])
        if select_table[0] == 'cities':
            update_param_table_cities_db(email_user, selected_key, value)
        elif select_table[0] == 'contact_details':
            update_param_table_contact_details_db(email_user, selected_key, value)
        elif select_table[0] == 'locations':
            update_param_table_locations_db(email_user, selected_key, value)
        elif select_table[0] == 'media_data':
            update_param_table_media_data_db(email_user, selected_key, value)
        elif select_table[0] == 'registration_data':
            update_param_table_registration_data_db(email_user, selected_key, value)
        elif select_table[0] == 'users':
            update_param_table_users_db(email_user, selected_key, value)
        print(email_user, selected_key, value, update_attr.get(selected_key))

        #update_param_db(email_user, update_attr.get(selected_key), value)
    except (ValueError, IndexError):
        print("Некорректный ввод. Пожалуйста, введите число от 1 до", len(options))


def exit_program():
    sys.exit()
