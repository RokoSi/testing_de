from pydantic import BaseModel

from src.json_parsing.model.coordinates import Coordinates
from src.json_parsing.model.street import Street


class Location(BaseModel):
    street: Street
    city: str
    state: str
    country: str
    postcode: int
    coordinates: Coordinates