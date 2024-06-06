import json
from pprint import pprint
import requests


def get_users_url(
    count_users: int, url: str = "https://randomuser.me/api/?results="
) -> [dict | bool]:
    with requests.get(url + str(count_users)) as response:
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return False


