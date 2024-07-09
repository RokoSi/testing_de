from typing import List, Dict, Union, Optional, Callable

from src.db_use.user_update import update_param_table_cities_db, update_param_table_contact_details_db, \
    update_param_table_locations_db, update_param_table_media_data_db, update_param_table_registration_data_db, \
    update_param_table_users_db
from src.settings import Settings


def update_param(settings: Settings) -> bool:
    """
    Изменение параметров
    :param settings: Данные для подключения к бд
    :return: Ture - если данные успешно изменены, False - если ошибка изменения данных
    """
    update_attr: Dict[str, List[str]] = {
        "city": ["cities"],
        "state": ["cities"],
        "country": ["cities"],
        "phone": ["contact_details"],
        "cell": ["contact_details"],
        "street_name": ["locations"],
        "street_number": ["locations"],
        "postcode": ["locations"],
        "latitude": ["locations"],
        "longitude": ["locations"],
        "picture": ["media_data"],
        "email": ["registration_data"],
        "username": ["registration_data"],
        "password": ["registration_data"],
        "password_md5": ["registration_data"],
        "gender": ["users"],
        "name_title": ["users"],
        "name_first": ["users"],
        "name_last": ["users"],
        "age": ["users"],
        "nat": ["users"],
    }
    print(
        *[f"{i}. {key}" for i, key in enumerate(update_attr.keys(), start=1)], sep="\n"
    )
    try:
        num_param: int = int(input("выберите параметр на изменение:"))
        options: List[str] = list(update_attr.keys())

        if num_param < 1 or num_param > len(options):
            raise IndexError(
                "Выбранный номер параметра выходит за пределы допустимого диапазона"
            )

        selected_key: str = options[int(num_param) - 1]
        print("Вы выбрали параметр:", selected_key)

        value: Union[str, int] = input("На что поменять: ")
        email_user: str = input("Выберете пользователя по email: ")
        select_table: Optional[List[str]] = update_attr.get(selected_key)

        if select_table is None:
            print("Не удалось найти таблицу для обновления")
            return False

        update_functions: Dict[str, Callable] = {
            "cities": update_param_table_cities_db,
            "contact_details": update_param_table_contact_details_db,
            "locations": update_param_table_locations_db,
            "media_data": update_param_table_media_data_db,
            "registration_data": update_param_table_registration_data_db,
            "users": update_param_table_users_db,
        }

        if select_table[0] in update_functions:
            if update_functions[select_table[0]](
                    settings, email_user, selected_key, value
            ):
                print("успешно")
                return True
            else:
                print("не успешно")
                return False
        return False
    except (ValueError, IndexError):
        print("Некорректный ввод. Пожалуйста, введите число от 1 до", len(update_attr))
        return False
