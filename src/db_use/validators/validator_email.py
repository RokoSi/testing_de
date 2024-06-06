from pydantic import EmailStr, ValidationError, BaseModel


class EmailModel(BaseModel):
    email: EmailStr


def validator_email(email: str):
    try:
        EmailModel(email=email)
        return True
    except ValidationError as e:
        return False
