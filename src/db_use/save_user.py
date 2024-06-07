from settings import Settings
from src.db_use.data_provider import connect_db
from src.json_parsing.model.users import Users
from src.validators.validator_password import validator_pass


def save_user(setting: Settings, person: Users) -> bool:
    """
    Сохранение пользователя
    :param setting: Данные для подключения
    :param person: все параметры пользователя
    :return: True - если удалось добавить пользователя, False - если пользователь не добавлен
    """
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
