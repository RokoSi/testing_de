from typing import Dict, List, Union

from src.db_use import get_users_db
from src.settings import Settings


def invalid_users(settings: Settings) -> bool:
    """
    Получение не валидных пользователей и их вывод
    :param settings: Данные для подключения к бд
    :return: Ture - если удалось найти таких пользователй,
     False - если не удалось найти таких пользователей
    """
    results: Union[List[Dict], bool] = get_users_db(settings, False)
    if isinstance(results, list):
        if results:
            for row in results:
                print(", ".join(map(str, row)))
            return True
        else:
            print("нет таких записей")
            return False
    else:
        print("Ошибка при получении данных")
        return False
