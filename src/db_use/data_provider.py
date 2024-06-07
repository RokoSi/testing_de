import psycopg2
from psycopg2 import OperationalError, ProgrammingError, DatabaseError

from src.db_use.ddl import ddl_use_string
from src.json_parsing.model.users import Users
from src.validators.validator_email import validator_email
from src.validators.validator_password import validator_pass
from src.settings import Settings


def decorator_get_users_db(func) -> [dict, bool]:
    def wrapper(query: str, param) -> [dict, bool]:
        try:
            return func(query, param)

        except OperationalError as oe:
            # log.error(f"Ошибка подключения к базе данных: {oe}")
            return False
        except psycopg2.errors.UniqueViolation as e:
            # log.info(f"Ошибка уникального ограничения:{e} Данные не будут добавлены")
            return False
        except ProgrammingError as pe:
            if str(pe) != 'ОШИБКА:  отношение "contact_details" уже существует\n':
                # log.error(f"Ошибка в SQL запросе: {pe}")
                return False
        except DatabaseError as de:
            # log.error(f"Ошибка базы данных: {de}")
            return False
        except Exception as e:
            # log.error(f"Произошла ошибка: {e}")
            return False

    return wrapper


@decorator_get_users_db
def connect_db(setting: Settings, query: str, param: tuple = None) -> [dict | bool]:
    with psycopg2.connect(
        host=setting.host,
        user=setting.user,
        password=setting.password,
        database=setting.db,
    ) as connection:
        connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(query, param)

        if cursor.description is not None:

            return cursor.fetchall()
        else:
            return cursor.rowcount


def create_db(setting) -> bool:
    query: str = (
        "SELECT COUNT(*) FROM pg_catalog.pg_tables WHERE schemaname NOT IN ('pg_catalog',"
        "'information_schema')"
    )

    count_table: [list | bool] = connect_db(setting, query)
    if type(count_table) is list:
        if count_table[0][0] != 0:
            try:
                connect_db(setting, ddl_use_string())
                return True
            except FileNotFoundError as fe:
                # log.error(f"Ошибка пути: {fe}")
                print(fe)
                return False
        return False
    return False


def save_user(setting, person: Users):
    insert_query_cities: str = (
        "INSERT INTO cities(city, state, country) VALUES (%s, %s, %s ) RETURNING city_id"
    )
    param_cities: tuple = (
        person.location.city,
        person.location.state,
        person.location.country,
    )

    city: dict = connect_db(setting, insert_query_cities, param_cities)
    if city:
        city_id: int = city[0][0]
        insert_query_users: str = (
            "INSERT INTO users(gender, name_title, name_first, name_last, age, nat) VALUES ("
            "%s, %s, %s, %s, %s, %s)RETURNING user_id"
        )
        param_users: tuple = (
            person.gender,
            person.name.title,
            person.name.first,
            person.name.last,
            person.registered.age,
            person.nat,
        )

        user: [dict | bool] = connect_db(setting, insert_query_users, param_users)
        user_id: int = user[0][0]

        insert_query_contact_details: str = (
            "INSERT INTO contact_details (user_id, phone, cell) VALUES (%s,%s,%s)"
        )
        param_contact_details: tuple = (user_id, person.phone, person.cell)

        connect_db(setting, insert_query_contact_details, param_contact_details)

        insert_query_media_data: str = (
            "INSERT INTO media_data(user_id, picture) VALUES (%s, %s)"
        )
        param_media_data: tuple = (user_id, person.picture.thumbnail)

        connect_db(setting, insert_query_media_data, param_media_data)

        insert_query_registration_data: str = (
            "INSERT INTO registration_data (user_id, email, username, password, "
            "password_md5, password_validation)VALUES (%s, %s, %s, %s, %s, %s)"
        )

        param_registration_data: tuple = (
            user_id,
            person.email,
            person.login.username,
            person.login.password,
            person.login.md5,
            validator_pass(person.login.password),
        )

        connect_db(setting, insert_query_registration_data, param_registration_data)

        insert_query_locations: str = (
            "INSERT INTO locations (user_id, city_id, street_name, street_number, "
            "postcode, latitude, longitude)VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )

        param_locations: tuple = (
            user_id,
            city_id,
            str(person.location.street.name),
            person.location.street.number,
            person.location.postcode,
            person.location.coordinates.latitude,
            person.location.coordinates.longitude,
        )

        connect_db(setting, insert_query_locations, param_locations)
        return True
    return False


def get_users_db(setting: Settings, param: bool) -> [dict | bool]:
    query: str = (
        "SELECT gender, name_title, name_first, name_last, age, nat, phone, cell, picture, email, username, "
        "password, password_md5, password_validation, city, state, country, street_name, street_number, "
        "postcode, latitude, longitude FROM users JOIN contact_details ON users.user_id = "
        "contact_details.user_id JOIN media_data ON users.user_id = media_data.user_id JOIN "
        "registration_data ON users.user_id = registration_data.user_id  JOIN locations ON users.user_id = "
        "locations.user_id JOIN cities ON locations.city_id=cities.city_id  WHERE "
        "registration_data.password_validation = %s"
    )
    param: tuple = (param,)
    return connect_db(setting, query, param)


def get_check_email(setting: Settings, email: str) -> [dict | bool]:
    if validator_email(email):
        query: str = "SELECT * FROM REGISTRATION_DATA WHERE EMAIL = %s"
        email = (email,)
        result = connect_db(setting, query, email)
        if len(result):
            return True
        else:
            return False
    else:
        print(f"email {email} не валиден")
    return False


def update_param_table_locations_db(
    setting: Settings, email: str, name_param: str, value: [str | float | int]
) -> [dict | bool]:
    """
    Метод для обновления данных в таблице locations
    :param setting:
    :param email: email пользователя
    :param name_param: имя атрибута, который надо изменить
    :param value: новое надо изменить
    :return: dict - если данные изменены, False - если нет
    """
    query: str = (
        f"UPDATE locations SET {name_param} = %s WHERE user_id = (SELECT user_id FROM registration_data "
        f"WHERE email =%s)"
    )
    param: tuple = (value, email)
    return connect_db(setting, query, param)


def update_param_table_cities_db(
    setting: Settings, email, name_param, value
) -> [dict | bool]:
    """
    Метод для обновления данных в таблице cities

    :param setting:
    :param email: email пользователя
    :param name_param: имя атрибута, который надо изменить
    :param value: новое значение
    :return: dict - если данные изменены, False - если нет
    """
    query: str = (
        f"UPDATE cities SET {name_param} = %s WHERE city_id = (SELECT city_id FROM locations WHERE user_id "
        f"= (SELECT user_id FROM registration_data WHERE email = %s) )"
    )
    param: tuple = (value, email)
    return connect_db(setting, query, param)


def update_param_table_registration_data_db(
    setting: Settings, email, name_param, value
) -> [dict | bool]:
    """
    Метод для обновления данных в таблице registration_data

    :param setting:
    :param email: email пользователя
    :param name_param: имя атрибута, который надо изменить
    :param value: новое значение
    :return: dict - если данные изменены, False - если нет
    """
    query: str = f"UPDATE registration_data SET {name_param} = %s WHERE email = %s"
    param: tuple = (value, email)
    return connect_db(setting, query, param)


def update_param_table_media_data_db(
    setting: Settings, email, name_param, value
) -> [dict | bool]:
    """
    Метод для обновления данных в таблице media_data

    :param setting:
    :param email: email пользователя
    :param name_param: имя атрибута, который надо изменить
    :param value: новое значение
    :return: dict - если данные изменены, False - если нет
    """
    query: str = (
        f"UPDATE media_data SET {name_param} = %s WHERE user_id =  (SELECT user_id FROM registration_data "
        f"WHERE email = %s)"
    )
    param: tuple = (value, email)
    return connect_db(setting, query, param)


def update_param_table_contact_details_db(
    setting: Settings, email, name_param, value
) -> [dict | bool]:
    """
    Метод для обновления данных в таблице contact_details

    :param setting:
    :param email: email пользователя
    :param name_param: имя атрибута, который надо изменить
    :param value: новое значение
    :return: dict - если данные изменены, False - если нет
    """
    query: str = (
        f"UPDATE contact_details SET {name_param} = %s WHERE user_id = ( SELECT user_id FROM "
        f"registration_data WHERE email = %s)"
    )
    param: tuple = (value, email)
    return connect_db(setting, query, param)


def update_param_table_users_db(
    setting: Settings, email, name_param, value
) -> [dict | bool]:
    """
    Метод для обновления данных в таблице users

    :param setting:
    :param email: email пользователя
    :param name_param: имя атрибута, который надо изменить
    :param value: новое значение
    :return: dict - если данные изменены, False - если нет
    """
    query: str = (
        f"UPDATE users SET {name_param} = %s WHERE user_id = ( SELECT user_id FROM registration_data WHERE "
        f"email = %s)"
    )
    param: tuple = (value, email)
    return connect_db(setting, query, param)


def del_user(setting: Settings, email: str):

    query_check_email: str = "SELECT email FROM registration_data   WHERE " "email = %s"
    param_email: tuple = (email,)
    check = connect_db(setting, query_check_email, param_email)
    if bool(len(check)):
        query_del: str = (
            f"""DELETE FROM registration_data
    WHERE email = %s;

    DELETE FROM locations
    WHERE user_id IN (
        SELECT user_id
        FROM registration_data
        WHERE email = %s
        LIMIT 1
    );

    DELETE FROM contact_details
    WHERE user_id IN (
        SELECT user_id
        FROM registration_data
        WHERE email = %s
        LIMIT 1
    );

    DELETE FROM media_data
    WHERE user_id IN (
        SELECT user_id
        FROM registration_data
        WHERE email = %s
        LIMIT 1
    );

    DELETE FROM users
    WHERE user_id IN (
        SELECT user_id
        FROM registration_data
        WHERE email = %s
        LIMIT 1
    );"""
        )
        param: tuple = (email, email, email, email, email)
        try:
            dd = connect_db(setting, query_del, param)
            return True
        except psycopg2.Error as e:
            print(f"Error deleting user: {e}")
            return False
    else:
        return False
