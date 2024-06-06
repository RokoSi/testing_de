from pydantic import BaseModel

from src.json_parsing.model.dob import Dob
from src.json_parsing.model.location import Location
from src.json_parsing.model.media_data import MediaData
from src.json_parsing.model.name import Name
from src.json_parsing.model.registered import Registered
from src.json_parsing.model.registration_data import RegistrationData


class Users(BaseModel):
    gender: str
    name: Name
    location: Location
    dob: Dob
    nat: str
    email: str
    login: RegistrationData
    registered: Registered
    phone: str
    cell: str
    picture: MediaData
