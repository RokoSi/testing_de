from pydantic import EmailStr, ValidationError, BaseModel


class EmailModel(BaseModel):
    email: EmailStr


def validator_email(email : str):
    try:
        EmailModel(email=email)
        return True
    except ValidationError as e:
        return False


if __name__ == "__main__":


    valid_email = validator_email("example@email.com")
    print( valid_email)

    invalid_email = validator_email("exampleemail.com")
    print(invalid_email)
