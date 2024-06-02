import re


def validator_password(password: str) -> bool:
    """
    Проверяет пароль.

    Проверяет пароль с помощью регулярного выражения.

    Param:
        password (str): пароль.

    return:
        bool: если пароль валидный вернет True, если нет, то False.
    """
    pattern = r'^(?=.*[A-Z])' r'(?=.*[a-z])' r'(?=.*[0-9])' r'(?=.*[!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~])'
    return re.search(pattern, password) is not None
