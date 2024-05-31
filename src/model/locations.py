from datetime import datetime
from pydantic import BaseModel


class locations(BaseModel):
    user_id: int
    city_id: int
    street_name: str
    street_number: int
    postcode: str
    latitude: int
    longitude: int
    created_dttm: datetime
    updated_dttm: datetime

    # def __init__(self, user_id, city_id,street_name, street_number, postcode, latitude, longitude, created_dttm, updated_dttm):
    #     self.user_id: int = user_id
    #     self.city_id: int = city_id
    #     self.street_name: str = street_name
    #     self.street_number: int = street_number
    #     self.postcode: str = postcode
    #     self.latitude: int = latitude
    #     self.longitude: int = longitude
    #     self.created_dttm = created_dttm
    #     self.updated_dttm = updated_dttm
