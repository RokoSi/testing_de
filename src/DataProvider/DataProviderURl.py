import logging
from pprint import pprint
import requests

from src.DataProvider.DataProviderDB import save_user

log = logging.getLogger(__name__)


def decorator_get_users_url(func):
    def wrapper(count_users: int, url: str) -> [dict | bool]:
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
        except requests.exceptions.RequestException as e:
            log.error(f"Неизвестная ошибка: {e}")
            return False

    return wrapper


@decorator_get_users_url
def get_users_url(count_users: int, url: str) -> [dict | bool]:
    with requests.get(url + str(count_users)) as response:
        if response.status_code == 200:
            data = response.json()

            return data
        else:
            return False


def parsing_json_file(json_data: dict):
    for result in json_data['results']:
        pprint(result)
        user_data = (result['gender'], result['name']['title'], result['name']['first'], result['name']['last'],
                     result['dob']['age'], result['nat'])
        contact_data = (result['phone'], result['cell'])
        media_data = result['picture']['large']
        registration_data = result['email'], result['login']['username'], result['login']['password'], result['login'][
            'md5']
        city_data = (result['location']['city'], result['location']['state'], result['location']['country'],)
        location_data = (result['location']['street']['name'],
                         result['location']['street']['number'], result['location']['postcode'],
                         result['location']['coordinates']['latitude'], result['location']['coordinates']['longitude'])

    save_user()
