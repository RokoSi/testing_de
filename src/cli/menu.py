from src.db_use.dataProvider import save_user, create_db
from src.json_parsing.get_user import get_users_url
from src.json_parsing.pars import pars_user


def main_menu(settings) -> tuple:
    menu_elements: [list] = [
        "1. Добавить пользователей",
        "2. Получить валидных пользователей",
        "3. Получить невалидных пользователей",
        "4. Проверить наличие email",
        "5. Изменение данных",
        "6. Выйти",
    ]
    print("Меню:")

    create_db(settings)

    choices_part_func = {
        1: count_user_add_menu
        # 2:
        # 3:
        # 4:
        # 5:
        # 6:
    }
    for item in menu_elements:
        print(item)

    while True:
        try:
            choice: int = int(input("Выберите пункт меню: "))
            print()
            return count_user_add_menu(settings)
        except ValueError:
            print("введите число")


def count_user_add_menu(settings) -> [tuple | bool]:
    while True:
        try:
            count_user = int(input("введите количество пользователей: "))
            json = get_users_url(count_user)
            users = pars_user(json)
            if not users:
                return False
            for user_param in range(len(users)):
                save_user(settings, users[user_param])

            return True
        except TypeError:
            return False
        except ValueError:
            print("введите число")
