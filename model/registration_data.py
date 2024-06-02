from datetime import datetime
from pydantic import BaseModel


class Registration_data(BaseModel):
    user_id: int
    email: str
    username: str
    password: str
    password_md5: str
    password_validation: bool
    created_dttm: datetime
    updated_dttm: datetime

    # def __int__(self, user_id, email, username, password, password_md5, password_validation,
    #             created_dttm, updated_dttm):
    #     self.user_id: int = user_id
    #     self.email: str = email
    #     self.username: str = username
    #     self.password: str = password
    #     self.password_md5: str = password_md5
    #     self.password_validation: bool = password_validation
    #     self.created_dttm = created_dttm
    #     self.updated_dttm = updated_dttm
