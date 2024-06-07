import logging

from src.json_parsing.model.users import Users

log = logging.getLogger(__name__)


def pars_user(dict_param: dict) -> [Users | bool]:
    """
    Парсинг полученного dict.
    :param dict_param: json приведенный к dict
    :return: Users - если удалось распарить | bool - если не удалось распарсить
    """
    try:

        users: list = [Users(**user) for user in dict_param]
        return users

    except (TypeError, KeyError, ValueError) as e:
        log.error(f"Ошибка {e}")
        return False
