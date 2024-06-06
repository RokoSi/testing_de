# -*- coding: utf-8 -*-
from settings import Settings
from src.cli import menu
from src.settings import settings


# from src.cli import menu


def main():

    part_menu = menu.main_menu(settings)


if __name__ == "__main__":
    main()
