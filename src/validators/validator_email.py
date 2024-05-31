import re


def validator_email(email) -> bool:
    email_regex = re.compile(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")

    return re.match(email_regex, email) is not None
