import re


def validator_email(email) -> bool:
    """
     Проверяет email.

    Проверяет email с помощью регулярного выражения.

    Param:
        email (str): email.

    return:
        bool: если email валидный вернет True, если нет, то False.
    """
    
    email_regex = re.compile(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")

    return re.match(email_regex, email) is not None
