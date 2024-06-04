from pydantic import BaseModel


class Users(BaseModel):
    gender: str
    name_title: str
    name_first: str
    name_last: str
    age: str
    nat: str
