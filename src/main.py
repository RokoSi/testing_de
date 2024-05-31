# -*- coding: utf-8 -*-
import logging
from src.DataProvider.DataProviderDB import create_db
from src.method_of_menu import add_users, change_url, get_valid_users, get_invalid_users, email_check, exit_program, \
    update_param

log = logging.getLogger(__name__)

formatlog = '%(asctime)s : %(name)s : %(levelname)s : %(message)s'
file_handler = logging.FileHandler(".\\logs\\log.log")#C:\\Users\\yur-f\\Desktop\\project\\test_de2\\src\\logs\\log.log")
file_handler.setLevel(logging.DEBUG)

logging.basicConfig(
    level=logging.DEBUG,
    format= formatlog,
    handlers=[file_handler],
  #  filemode='w'
)



def print_menu():
    print("Меню:")
    print("1. Добавить пользователей")
    print("2. Изменить URL")
    print("3. Получить валидных пользователей")
    print("4. Получить невалидных пользователей")
    print("5. проверить наличие email:")
    print("6: изменение данных")
    print("7. Выйти")


def menu_choice(choice):
    choices = {
        1: add_users,
        2: change_url,
        3: get_valid_users,
        4: get_invalid_users,
        5: email_check,
        6: update_param,
        7: exit_program
    }
    action = choices.get(choice)
    action()


def main():
    create_db()

    while True:

        try:
            print_menu()
            choice = int(input("Выберите пункт меню: "))

            menu_choice(choice)
        except ValueError:
            print("введите число, а не str: ")


if __name__ == '__main__':
    main()
