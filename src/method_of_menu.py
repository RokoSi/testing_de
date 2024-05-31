import sys

from src.DataProvider.DataProviderURl import get_users_url,  parsing_and_save_file


url = "https://randomuser.me/api/?results="


def get_url():
    return url


def set_url(new_url):
    global url
    url = new_url


def add_users() -> bool:
    count_user_in_db: int = 0
    exit_add: bool = True
    while exit_add:
        try:
            count: int = int(input("введите количество пользователей: "))
            if count:
                json_file: [dict | bool] = get_users_url(count, url)
                count_user_in_db: int = parsing_and_save_file(json_file)
            print("Успешно добавлено: ", count_user_in_db, "записей")
            exit_add = False
            return True
        except ValueError:
            print("ОШИБКА: ведите число:  ")
    return False


def change_url():
    new_url = input("введите корректный url: ")
    set_url(new_url)
    print("\n url изменен \n", get_url())


#
# def get_invalid_users():
#     results = get_users_db(False)
#     if len(results) != 0:
#         for row in results:
#             print(", ".join(map(str, row)))
#     else:
#         print("нет таких записей")
#
#
# def get_valid_users():
#     results = get_users_db(True)
#     if len(results) != 0:
#         for row in results:
#             print(", ".join(map(str, row)))
#     else:
#         print("нет таких записей\n")
#
#
# def email_check():
#     email: str = input("введите email:")
#     answer_email: list = get_chek_email(email)
#     if len(answer_email) == 0:
#         print("нет такого email в базе\n")
#     else:
#         print("есть такой email в базе\n")

#
# def update_param():
#     print(*[f"{i}. {key}" for i, key in enumerate(update_attr.keys(), start=1)], sep='\n')
#     num_param = input("выберите параметр на изменение:")
#     try:
#         options = list(update_attr.keys())
#         selected_key = options[int(num_param) - 1]
#         print("Вы выбрали параметр:", selected_key)
#
#         value = input("На что поменять: ")
#         email_user = input("Выберете пользователя по email: ")
#
#         select_table = update_attr.get(selected_key)
#         print(select_table[0])
#         if select_table[0] == 'cities':
#             update_param_table_cities_db(email_user, selected_key, value)
#         elif select_table[0] == 'contact_details':
#             update_param_table_contact_details_db(email_user, selected_key, value)
#         elif select_table[0] == 'locations':
#             update_param_table_locations_db(email_user, selected_key, value)
#         elif select_table[0] == 'media_data':
#             update_param_table_media_data_db(email_user, selected_key, value)
#         elif select_table[0] == 'registration_data':
#             update_param_table_registration_data_db(email_user, selected_key, value)
#         elif select_table[0] == 'users':
#             update_param_table_users_db(email_user, selected_key, value)
#         print(email_user, selected_key, value, update_attr.get(selected_key))
#
#         #update_param_db(email_user, update_attr.get(selected_key), value)
#     except (ValueError, IndexError):
#         print("Некорректный ввод. Пожалуйста, введите число от 1 до", len(options))
#

def exit_program():
    sys.exit()
