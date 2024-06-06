# -*- coding: utf-8 -*-
from settings import settings
from src.cli import menu


def main():
    part_menu = menu.main_menu()
    print(settings.url)
    print(part_menu)


if __name__ == "__main__":
    main()
