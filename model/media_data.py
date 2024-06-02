from datetime import datetime
from pydantic import BaseModel


class media_data(BaseModel):
    user_id: int
    picture: str
    created_dttm: datetime
    updated_dttm: datetime

    # def __init__(self, user_id, picture, created_dttm, updated_dttm):
    #     self.user_id: int = user_id
    #     self.picture: str = picture
    #     self.created_dttm = created_dttm
    #     self.updated_dttm = updated_dttm