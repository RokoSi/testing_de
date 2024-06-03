import logging
import os

import psycopg2
from psycopg2 import OperationalError, ProgrammingError, DatabaseError

from Settings import Settings
from src.validators.validator_email import validator_email
from src.validators.validator_password import validator_password

log = logging.getLogger(__name__)
settings = Settings()


def decorator_get_users_db(func: callable) -> callable:
    def wrapper(query: str, param: tuple = None) -> [dict | bool]:
        """
            Декоратор для подключения к бд, служит для обработки ошибок

            :param query: запрос на подключение
            :param param: параметры для запроса
            :return: вернет dict если выполнится без ошибок, если нет, то False и записывает ошибку в log файл
            """
        try:
            return func(query, param)

        except OperationalError as oe:
            log.error(f"Ошибка подключения к базе данных: {oe}")
            return False
        except psycopg2.errors.UniqueViolation as e:
            log.info(f"Ошибка уникального ограничения:{e} Данные не будут добавлены")
            return False
        except ProgrammingError as pe:
            if str(pe) != 'ОШИБКА:  отношение "contact_details" уже существует\n':
                log.error(f"Ошибка в SQL запросе: {pe}")
                return False
        except DatabaseError as de:
            log.error(f"Ошибка базы данных: {de}")
            return False
        except Exception as e:
            log.error(f"Произошла ошибка: {e}")
            return False

    return wrapper


@decorator_get_users_db
def connect_db(query: str, param: tuple = None) -> [dict | bool]:
    """
        Метод для подключения к бд

        :param query: запрос на подключение
        :param param: параметры для запроса
        :return: если возвращает значение, то вернет возвращаемое значение, если нет, то False
        """
    with psycopg2.connect(
            host=settings.host,
            user=settings.user,
            password=settings.password,
            database=settings.db) as connection:
        connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(query, param)

        if cursor.description is not None:
            return cursor.fetchall()
        else:
            return False


def create_db() -> bool:
    """
        Метод для создания таблиц в бд

        :return: если таблицы созданы вернет True, если ошибка, то False
        """
    query: str = ("SELECT COUNT(*) FROM pg_catalog.pg_tables WHERE schemaname NOT IN ('pg_catalog',"
                  "'information_schema')")

    count_table: [list | bool] = connect_db(query)
    if type(count_table) is list:
        if count_table[0][0] != 0:
            try:
                db_dir = os.path.join(os.getcwd(), "db")
                ddl_file = os.path.join(db_dir, "DDL.sql")

                with open(f'{ddl_file}', 'r') as file:
                    sql_script: str = file.read()
                connect_db(sql_script)
                return True
            except FileNotFoundError as fe:
                log.error(f"Ошибка пути: {fe}")
                return False
        return False
    return False


def save_user(person: tuple) -> bool:
    """
        Метод для сохранения пользователя в бд

        :param person: данные в формате tuple, которые содержат всю информацию о пользователе
        :return: True - если сохранение выполнено, False - если нет """
    query: str = "INSERT INTO cities(city, state, country) VALUES (%s, %s, %s ) RETURNING city_id"
    param: tuple = (person[0][0], person[0][1], person[0][2])

    city: dict = connect_db(query, param)

    if city:
        city_id: int = city[0][0]
        query: str = ("INSERT INTO users(gender, name_title, name_first, name_last, age, nat) VALUES (%s, %s, %s, %s, "
                      "%s, %s)RETURNING user_id")
        param: tuple = (person[1][0], person[1][1], person[1][2], person[1][3], person[1][4], person[1][5])
        user: [dict | bool] = connect_db(query, param)
        user_id: int = user[0][0]

        query: str = "INSERT INTO contact_details (user_id, phone, cell) VALUES (%s,%s,%s)"
        param: tuple = (user_id, person[2][0], person[2][1])

        connect_db(query, param)

        query: str = "INSERT INTO media_data(user_id, picture) VALUES (%s, %s)"
        param: tuple = (user_id, person[3])
        connect_db(query, param)

        query: str = ("INSERT INTO registration_data (user_id, email, username, password, password_md5, "
                      "password_validation)VALUES (%s, %s, %s, %s, %s, %s)")
        param: tuple = (
            user_id, person[4][0], person[4][1], person[4][2], person[4][3], validator_password(person[4][1]))

        connect_db(query, param)

        query: str = ("INSERT INTO locations (user_id, city_id, street_name, street_number, postcode, latitude, "
                      "longitude)VALUES (%s, %s, %s, %s, %s, %s, %s)")
        param: tuple = (user_id, city_id, str(person[5][0]), person[5][1], person[5][2], person[5][3], person[5][4])

        connect_db(query, param)
        return True
    return False


def get_users_db(param: bool) -> [dict | bool]:
    """
        Получение списка пользователей с валидным или не валидным паролем

        :param param: bool параметр False - не валидные пользователи, True - валидные пользователи
        :return: dict - если пользователи такие есть, False - если таких нет
        """
    query: str = ("SELECT gender, name_title, name_first, name_last, age, nat, phone, cell, picture, email, username, "
                  "password, password_md5, password_validation, city, state, country, street_name, street_number, "
                  "postcode, latitude, longitude FROM users JOIN contact_details ON users.user_id = "
                  "contact_details.user_id JOIN media_data ON users.user_id = media_data.user_id JOIN "
                  "registration_data ON users.user_id = registration_data.user_id  JOIN locations ON users.user_id = "
                  "locations.user_id JOIN cities ON locations.city_id=cities.city_id  WHERE "
                  "registration_data.password_validation = %s")
    param: tuple = (param,)
    return connect_db(query, param)


def get_check_email(email: str) -> [dict | bool]:
    """
        Проверяет, если ли пользовать с таким email в бд, так же проверяет на валидность пароля
        :param email: email пользователя
        :return: dict - если пользователь найдет, False - если нет
        """
    if validator_email(email):
        query: str = "SELECT * FROM REGISTRATION_DATA WHERE EMAIL = %s"
        email = (email,)
        return connect_db(query, email)
    else:
        print(f"email {email} не валиден")
    return False


def update_param_table_locations_db(email: str, name_param: str, value: [str | float | int]) -> [dict | bool]:
    """
        Метод для обновления данных в таблице locations
        :param email: email пользователя
        :param name_param: имя атрибута, который надо изменить
        :param value: новое надо изменить
        :return: dict - если данные изменены, False - если нет
        """
    query: str = (f"UPDATE locations SET {name_param} = %s WHERE user_id = (SELECT user_id FROM registration_data "
                  f"WHERE email =%s)")
    param: tuple = (value, email)
    return connect_db(query, param)


def update_param_table_cities_db(email, name_param, value) -> [dict | bool]:
    """
        Метод для обновления данных в таблице cities
        :param email: email пользователя
        :param name_param: имя атрибута, который надо изменить
        :param value: новое значение
        :return: dict - если данные изменены, False - если нет
        """
    query: str = (f"UPDATE cities SET {name_param} = %s WHERE city_id = (SELECT city_id FROM locations WHERE user_id "
                  f"= (SELECT user_id FROM registration_data WHERE email = %s) )")
    param: tuple = (value, email)
    return connect_db(query, param)


def update_param_table_registration_data_db(email, name_param, value) -> [dict | bool]:
    """
        Метод для обновления данных в таблице registration_data
        :param email: email пользователя
        :param name_param: имя атрибута, который надо изменить
        :param value: новое значение
        :return: dict - если данные изменены, False - если нет
        """
    query: str = f"UPDATE registration_data SET {name_param} = %s WHERE email = %s"
    param: tuple = (name_param, value, email)
    return connect_db(query, param)


def update_param_table_media_data_db(email, name_param, value) -> [dict | bool]:
    """
        Метод для обновления данных в таблице media_data
        :param email: email пользователя
        :param name_param: имя атрибута, который надо изменить
        :param value: новое значение
        :return: dict - если данные изменены, False - если нет
        """
    query: str = (f"UPDATE media_data SET {name_param} = %s WHERE user_id =  (SELECT user_id FROM registration_data "
                  f"WHERE email = %s)")
    param: tuple = (name_param, value, email)
    return connect_db(query, param)


def update_param_table_contact_details_db(email, name_param, value) -> [dict | bool]:
    """
        Метод для обновления данных в таблице contact_details
        :param email: email пользователя
        :param name_param: имя атрибута, который надо изменить
        :param value: новое значение
        :return: dict - если данные изменены, False - если нет
        """
    query: str = (f"UPDATE contact_details SET {name_param} = %s WHERE user_id = ( SELECT user_id FROM "
                  f"registration_data WHERE email = %s)")
    param: tuple = (name_param, value, email)
    return connect_db(query, param)


def update_param_table_users_db(email, name_param, value) -> [dict | bool]:
    """
        Метод для обновления данных в таблице users
        :param email: email пользователя
        :param name_param: имя атрибута, который надо изменить
        :param value: новое значение
        :return: dict - если данные изменены, False - если нет
        """
    query: str = (f"UPDATE users SET {name_param} = %s WHERE user_id = ( SELECT user_id FROM registration_data WHERE "
                  f"email = %s)")
    param: tuple = (name_param, value, email)
    return connect_db(query, param)
