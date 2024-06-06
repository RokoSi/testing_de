import json
import requests


def get_users_url(
    count_users: int, url: str = "https://randomuser.me/api/?results="
) -> [dict | bool]:
    try:
        with requests.get(url + str(count_users)) as response:
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
