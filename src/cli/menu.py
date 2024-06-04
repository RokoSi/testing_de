def main_menu() -> tuple:
    menu_elements: [list] = [
        "1. Добавить пользователей",
        "2. Получить валидных пользователей",
        "3. Получить невалидных пользователей",
        "4. Проверить наличие email",
        "5. Изменение данных",
        "6. Выйти",
    ]
    print("Меню:")

    for item in menu_elements:
        print(item)

    while True:
        try:
            choice: int = int(input("Выберите пункт меню: "))
            return count_user_add_menu()
        except ValueError:
            print("введите число")


def count_user_add_menu() -> tuple:
    while True:
        try:
            count_user = int(input("введите количество пользователей: "))
            return 1, count_user
        except ValueError:
            print("введите число")
