# -*- coding: utf-8 -*-
import logging
import os
import sys

from src.DataProvider.DataProviderDB import create_db
from src.method_of_menu import add_users, change_url, get_valid_users, get_invalid_users, email_check, exit_program, \
    update_param

log = logging.getLogger(__name__)

log_dir = os.path.join(os.getcwd(), "logs")
log_file = os.path.join(log_dir, "logfile.log")

logging.basicConfig(filename=log_file,
                    filemode="w",
                    encoding="utf-8",
                    level=logging.DEBUG,
                    format='%(asctime)s : %(name)s : %(levelname)s : %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p')



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






if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()

