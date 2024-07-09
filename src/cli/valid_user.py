from typing import Union, List, Dict

from src.db_use import get_users_db
from src.settings import Settings


def valid_users(settings: Settings) -> bool:
    """
    Получение валидных пользователей и их вывод
    :param settings: Данные для подключения к бд
    :return: Ture - если удалось найти таких пользователй,
    False - если не удалось найти таких пользователей
    """
    results: Union[List[Dict], bool] = get_users_db(settings, True)
    if isinstance(results, list):
        if results:
            for row in results:
                print(", ".join(map(str, row)))
            return True
        else:
            print("нет таких записей\n")
            return False
    else:
        print("Ошибка при получении данных")
        return False
