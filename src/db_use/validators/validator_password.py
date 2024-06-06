import string


def validator_pass(password: str):
    if (any(char in string.punctuation for char in password) and any(char in string.digits for char in password)
            and any(char in string.ascii_uppercase for char in password) and any(
                char in string.ascii_lowercase for char in password)):
        return True
    else:
        return False


if __name__ == "__main__":
    print(validator_pass("rwerwefsdffA"))
