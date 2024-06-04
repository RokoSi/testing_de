# -*- coding: utf-8 -*-
from cli import menu
from src.option_switch.json_parsing.get_user import get_users_url
from src.option_switch.json_parsing.pars import pars_user
from settings import settings


def main():
    part_menu = menu.main_menu()
    print(settings.url)
    print(part_menu)


if __name__ == "__main__":
    main()
