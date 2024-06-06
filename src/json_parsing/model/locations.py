from pydantic import BaseModel


class Locations(BaseModel):
    street_name: str
    street_number: str
    postcode: str
    latitude: float
    longitude: float