
from datetime import datetime
from pydantic import BaseModel


class cities(BaseModel):
    city_id: int
    city: str
    state: str
    country: str
    created_dttm: datetime
    updated_dttm: datetime

    # def __int__(self, city_id, city, state, country, created_dttm, updated_dttm):
    #     self.city_id: int = city_id
    #     self.city: str = city
    #     self.state: str = state
    #     self.country: str = country
    #     self.created_dttm = created_dttm
    #     self.updated_dttm = updated_dttm
