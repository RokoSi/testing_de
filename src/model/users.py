from datetime import datetime
from pydantic import BaseModel


class users(BaseModel):
    #user_id: int
    gender: str
    name_title: str
    name_first: str
    name_last: str
    age: int
    nat: str
    # created_dttm: datetime
    # updated_dttm: datetime

    # def __init__(self, user_id, gender, name_title, name_first, name_last, age, nat, created_dttm, updated_dttm):
    #     self.user_id: int = user_id
    #     self.gender: str = gender
    #     self.name_title: str = name_title
    #     self.name_first: str = name_first
    #     self.name_last: str = name_last
    #     self.age: int = age
    #     self.nat: str = nat
    #     self.created_dttm = created_dttm
    #     self.updated_dttm = updated_dttm