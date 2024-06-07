import json
import requests
from settings import Settings


def get_users_url(count_users: int, settings: Settings) -> [dict | bool]:
    try:
        with requests.get(settings.url + str(count_users)) as response:
            if response.status_code == 200:
                data = response.json()

                return data["results"]
            else:
                return False
    except (requests.exceptions.RequestException, json.decoder.JSONDecodeError) as e:
        print(f"Ошибка: {e}")
        return False
    except (KeyError, TypeError) as e:
        print(f"Ошибка: {e}")
        return False
