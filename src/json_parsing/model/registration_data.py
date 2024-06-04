from pydantic import BaseModel


class RegistrationData(BaseModel):
    email: str
    username: str
    password: str
    password_md5: str
