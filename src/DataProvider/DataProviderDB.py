import logging
from datetime import datetime
import psycopg2
from psycopg2 import OperationalError, ProgrammingError, DatabaseError
from src.resources import constants
from src.validators.validator_password import validator_password

log = logging.getLogger(__name__)


def decorator_get_users_db(func):
    def wrapper(query: str):
        try:
            return func(query)

        except OperationalError as oe:
            log.error(f"Ошибка подключения к базе данных: {oe}")
            return False
        except psycopg2.errors.UniqueViolation as e:
            log.error("Ошибка уникального ограничения:", e.diag.message_detail, "Данные не будут добавлены")
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
def connect_db(query: str):
    with psycopg2.connect(
            host=constants.HOST,
            user=constants.USER,
            password=constants.PASSWORD,
            database=constants.DB) as connection:
        connection.autocommit = True  # Установка autocommit внутри контекстного менеджера

    with connection.cursor() as cursor:
        cursor.execute(query)
        if cursor.description is not None:
            return cursor.fetchall()
        else:
            return False


def create_db():
    query = """
    SELECT COUNT(*) FROM pg_catalog.pg_tables
    WHERE schemaname NOT IN ('pg_catalog', 'information_schema'); """

    count_table = connect_db(query)
    print("бд создана"
          )
    if count_table[0][0] == 0:
        # добавить проверку на кол-во таблиц, чтобы не читать файл
        try:
            with open('src/resources/DDL.sql', 'r') as file:
                sql_script = file.read()
            connect_db(sql_script)
        except FileNotFoundError as fe:
            print(f"Ошибка пути: {fe}")


def save_user(person: tuple):
    query = f"INSERT INTO cities(city, state, country, created_dttm, updated_dttm)VALUES ({person[4][0]}, {person[4][1]}, {person[4][2]} ) RETURNING city_id"
    city = connect_db(query)

    if city:
        city_id = city[0][0]
        query = (f"INSERT INTO users(gender, name_title, name_first, name_last, age, nat) "
                 f"VALUES ({person[0][0]},{person[0][1]},{person[0][2]},{person[0][3]},{person[0][4]},{person[0][
                     5]})RETURNING user_id")

        user = connect_db(query)
        user_id: int = user[0][0]

        query = f"INSERT INTO contact_details (user_id, phone, cell) VALUES ({user_id}, {person[1][0]}, {person[1][1]})"

        connect_db(query)

        query = f"INSERT INTO media_data(user_id, picture) VALUES ({user_id}, {person[2][0]})"
        connect_db(query)

        query = (f"INSERT INTO registration_data (user_id, email, username, password, password_md5, "
                 f"password_validation)VALUES ({user_id}, {person[3][0]}, {person[3][1]},{person[3][2]},{person[3][3]},"
                 f"{validator_password(person[3][1])}))")


#
#         connect_db(query)
#
#         query = """
#             INSERT INTO locations (user_id, city_id, street_name, street_number, postcode, latitude, longitude,
#             created_dttm, updated_dttm)
#             VALUES ({}, {}, '{}',{},'{}',{}, {}, '{}','{}')""".format(
#             user_id,
#             city_id,
#             data_dict['street_name'],
#             data_dict['street_number'],
#             data_dict['postcode'],
#             data_dict['latitude'],
#             data_dict['longitude'],
#             datetime.now(),
#             datetime.now()
#         )
#
#         connect_db(query)
#         return 1
#     return 0
#
#
# def get_users_db(param: bool):
#     query = """SELECT * FROM users
#     JOIN contact_details ON users.user_id = contact_details.user_id
#     JOIN media_data ON users.user_id = media_data.user_id
#     JOIN registration_data ON users.user_id = registration_data.user_id
#     JOIN locations ON users.user_id = locations.user_id
#     WHERE registration_data.password_validation = {}""".format(param)
#     return connect_db(query)
#
#
# def get_chek_email(email: str):
#     query = """SELECT * FROM REGISTRATION_DATA WHERE EMAIL = '{}'""".format(email)
#     return connect_db(query)
#
#
# #!1
# def update_param_table_locations_db(email, name_param, value):
#     query = """UPDATE locations SET {} = '{}' WHERE
#             user_id = (SELECT user_id FROM registration_data WHERE email = '{}')""".format(name_param, value, email)
#     connect_db(query)
#
#
# #!!
# def update_param_table_cities_db(email, name_param, value):
#     query = """UPDATE cities SET {} = '{}' WHERE city_id = (SELECT city_id FROM locations WHERE user_id = (SELECT
#             user_id FROM registration_data WHERE email = '{}') )""".format(name_param, value, email)
#     connect_db(query)
#
#
# #11
# def update_param_table_registration_data_db(email, name_param, value):
#     query = """UPDATE registration_data SET {} = '{}'
#             WHERE email = '{}'""".format(name_param, value, email)
#     connect_db(query)
#
#
# #11
# def update_param_table_media_data_db(email, name_param, value):
#     query = """UPDATE media_data SET {} = '{}'
#     WHERE user_id =  (SELECT user_id FROM registration_data WHERE email = '{}') """.format(name_param, value, email)
#     connect_db(query)
#
#
# #!!
# def update_param_table_contact_details_db(email, name_param, value):
#     query = """UPDATE contact_details SET {} = '{}' WHERE user_id = ( SELECT user_id FROM registration_data
#     WHERE email = '{}')  """.format(name_param, value, email)
#     connect_db(query)
#
#
# #!!
# def update_param_table_users_db(email, name_param, value):
#     query = """UPDATE users SET {} = '{}' WHERE user_id = ( SELECT user_id FROM registration_data
#     WHERE email = '{}')""".format(
#         name_param, value, email)
#     connect_db(query)
