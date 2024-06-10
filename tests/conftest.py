import pytest

from src.db_use.save_user import save_user
from src.json_parsing.model.coordinates import Coordinates
from src.json_parsing.model.dob import Dob
from src.json_parsing.model.location import Location
from src.json_parsing.model.media_data import MediaData
from src.json_parsing.model.name import Name
from src.json_parsing.model.registered import Registered
from src.json_parsing.model.registration_data import RegistrationData
from src.json_parsing.model.street import Street
from src.json_parsing.model.users import Users
from src.settings import Settings


@pytest.fixture
def user_data_test(setting_te: Settings):
    user = [Users(gender='Female',
                  name=Name(title='Miss',
                            first='wbucswjwgz',
                            last='xcdzwvzfby'),
                  location=Location(
                      street=Street(name='lifwrtgffssmjoi',
                                    number=8129),
                      city='zdcspdyqkf',
                      state='DP',
                      country='MX',
                      postcode=242,
                      coordinates=Coordinates(latitude=12708.0,
                                              longitude=-143.36881678369627)),
                  dob=Dob(age=32),
                  nat='JP',
                  email='twijkwiptm.oglnmerecx@gmail.com',
                  login=RegistrationData(username='gaw1s7ta',
                                         password='isJzpconQjM1',
                                         md5='49f8e838bd0b240320ad8e53d0bda2b6'),
                  registered=Registered(date='2014-01-20T17:20:35.041Z', age=10),
                  phone='389-2309-3994',
                  cell='946-5158-7970',
                  picture=MediaData(large='https://randomuser.me/api/portraits/men/18.jpg',
                                    medium='https://randomuser.me/api/portraits/med/men/18.jpg',
                                    thumbnail='https://randomuser.me/api/portraits/thumb/men/18.jpg'))]

    if save_user(setting_te, user[0]):
        return user


@pytest.fixture
def setting_te():
    return Settings(
        host="127.0.0.1",
        db="de_projects",
        user="admin",
        password="password",
        port=5432,
        url="https://randomuser.me/api/?password=special,upper,lower,number",
    )
