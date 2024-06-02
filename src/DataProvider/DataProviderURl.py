import logging
from pprint import pprint

import requests

from model.Settings import Settings
from src.DataProvider.DataProviderDB import save_user

log = logging.getLogger(__name__)
settings = Settings()


def decorator_get_users_url(func):
    def wrapper(count_users: int, url: str = settings.URL) -> [dict | bool]:
        try:
            return func(count_users, url)
        except requests.exceptions.MissingSchema:
            log.error("Ошибка: отсутствует схема в URL.")
            return False
        except requests.exceptions.InvalidURL:
            log.error("Ошибка: некорректный URL.")
            return False
        except requests.exceptions.ConnectionError:
            log.error("Ошибка: ошибка соединения.")
            return False
        except requests.exceptions.Timeout:
            log.info("Истекло время ожидания")
            return False
        except requests.exceptions.RequestException as e:
            log.error(f"Неизвестная ошибка: {e}")
            return False

    return wrapper


@decorator_get_users_url
def get_users_url(count_users: int, url: str = settings.URL) -> [dict | bool]:
    with requests.get(url + str(count_users)) as response:
        if response.status_code == 200:
            data = response.json()

            return data
        else:
            return False


def parsing_and_save_file(json_data: dict) -> int:
    count_add_users: int = 0
    pprint(json_data)
    try:
        for result in json_data['results']:
            user_data = (result['gender'], result['name']['title'], result['name']['first'], result['name']['last'],
                         result['dob']['age'], result['nat'])
            contact_data = (result['phone'], result['cell'])
            media_data = result['picture']['large']
            registration_data = (result['email'], result['login']['username'],
                                 result['login']['password'], result['login']['md5'])
            city_data = (result['location']['city'], result['location']['state'], result['location']['country'],)
            location_data = (result['location']['street']['name'],
                             result['location']['street']['number'], result['location']['postcode'],
                             result['location']['coordinates']['latitude'],
                             result['location']['coordinates']['longitude'])

            count_add_users += save_user(
                (city_data, user_data, contact_data, media_data, registration_data, location_data))
    except TypeError as te:
        log.error(f"{te}")

    return count_add_users
