# -*- coding: utf-8 -*-

from src.cli import menu
from src.settings import settings


def main():
    menu.main_menu(settings)


if __name__ == "__main__":
    main()
