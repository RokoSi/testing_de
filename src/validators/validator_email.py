import re


def validator_email(email) -> bool:
    email_regex = re.compile(
        r"^(?!.*\.{2})"  # Нет двойных точек
        r"(?!\.)(?!.*\.$)"  # Нет точки в начале и конце
        r"[a-zA-Z0-9._%+-]+"  # Имя пользователя
        r"@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"  # Доменное имя
    )

    return re.match(email_regex, email) is not None
