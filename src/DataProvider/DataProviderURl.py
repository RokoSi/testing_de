import json
from pprint import pprint

import requests
from typing import List

from pydantic import BaseModel

from src.model.users import users


def decorator_get_users_url(func):
    def wrapper(count_users: int, url: str) -> [dict | bool]:
        try:
            return func(count_users, url)
        except requests.exceptions.MissingSchema:
            print("Ошибка: отсутствует схема в URL.")
            return False
        except requests.exceptions.InvalidURL:
            print("Ошибка: некорректный URL.")
            return False
        except requests.exceptions.ConnectionError:
            print("Ошибка: ошибка соединения.")
            return False
        except requests.exceptions.RequestException as e:
            print(f"Неизвестная ошибка: {e}")
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





# def parsing_json_file(data):
#     dict_data: dict = {}
#     for key, path in parameters.items():
#         get_value = lambda results, path=path: eval("results" + "".join(f"['{x}']" for x in path))
#         value = get_value(data['results'][0])
#         dict_data[key] = value
#     return dict_data

#    return email[0], password[0]


def parsing_json_file(data):

    try:
        jdata = {"gender": "ппп",
    "name_title":" str",
    "name_first": "str",
    "name_last": "str",
    "age": 123,
    "nat": "str"}

        user_data = data['results'][0]
        pprint(user_data)
        j_str = json.dumps(user_data)
        user = users.parse_raw(j_str)




        pprint(user)
    except Exception as e:
        print("ошибка ", e )
