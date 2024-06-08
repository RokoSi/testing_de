import logging
from typing import Union, List, Dict

from settings import Settings
from src.db_use.data_provider import connect_db
from src.validators.validator_email import validator_email

log = logging.getLogger(__name__)


def get_users_db(setting: Settings, email: str) -> Union[List[Dict], bool]:
    """
    Получение user с помощью email
    :param setting: Данные для подключения к бд
    :param email: email для получения всех данный о пользователе
    :return: dict - все данные о пользователе, False - если не удалось получить данные пользователе
    """
    query: str = (
        "SELECT gender, name_title, name_first, name_last, age, nat, phone, cell, picture, email, username, "
        "password, password_md5, password_validation, city, state, country, street_name, street_number, "
        "postcode, latitude, longitude FROM users JOIN contact_details ON users.user_id = "
        "contact_details.user_id JOIN media_data ON users.user_id = media_data.user_id JOIN "
        "registration_data ON users.user_id = registration_data.user_id  JOIN locations ON users.user_id = "
        "locations.user_id JOIN cities ON locations.city_id=cities.city_id  WHERE "
        "registration_data.password_validation = %s"
    )
    param: tuple = (email,)
    return connect_db(setting, query, param)


def get_check_email(setting: Settings, email: str) -> bool:
    """
    Проверяет если ли такой пользователь в бд
    :param setting: Данные для подключения к бд
    :param email: email для проверки
    :return: True - если пользователь есть в бд, False - если такого пользователя нет
    """
    if validator_email(email):
        query: str = "SELECT * FROM REGISTRATION_DATA WHERE EMAIL = %s"
        email: tuple = (email,)
        result: [list] = connect_db(setting, query, email)
        if len(result):
            return True
        else:
            return False
    else:
        log.error(f"email {email} не валиден")
    return False
