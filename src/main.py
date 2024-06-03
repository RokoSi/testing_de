# -*- coding: utf-8 -*-
import logging
import os
import sys
from src.DataProvider.DataProviderDB import create_db
from src.method_of_menu import add_users, get_valid_users, get_invalid_users, email_check, update_param, exit_program
from resources.constants import MENU_ITEMS

log = logging.getLogger(__name__)

log_dir = os.path.join(os.getcwd(), "logs")
log_file = os.path.join(log_dir, "logfile.log")
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=log_file,
                    filemode="a",
                    encoding="utf-8",
                    level=logging.DEBUG,
                    format='%(asctime)s - %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p')


def menu_choice(choice):
    choices = {
        1: add_users,
        2: get_valid_users,
        3: get_invalid_users,
        4: email_check,
        5: update_param,
        6: exit_program
    }
    action = choices.get(choice)
    action()


def main():

    if create_db():

        while True:
            try:
                print("Меню:")
                for item in MENU_ITEMS:
                    print(item)
                choice = int(input("Выберите пункт меню: "))
                menu_choice(choice)
            except ValueError:
                print("введите число, а не str: ")
    else:
        print("Программа не смога найти или создать таблицы для работы с бд")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
