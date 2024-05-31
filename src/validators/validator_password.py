import re


def validator_password(password):
    pattern = r'^(?=.*[A-Z])' r'(?=.*[a-z])' r'(?=.*[0-9])' r'(?=.*[!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~])'
    return re.search(pattern, password) is not None
