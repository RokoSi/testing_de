import hashlib
import secrets
import string
import random
import pytest
from src.db_use.get_user import get_users_db
from src.db_use.user_update import (
    update_param_table_registration_data_db,
    update_param_table_media_data_db,
    update_param_table_contact_details_db,
    update_param_table_users_db,
    update_param_table_locations_db,
    update_param_table_cities_db,
)


class TestDataProviderDB:
    def random_update_param_table_users_db(self):
        param_functions = {
            "gender": self.random_gender,
            "name_title": self.random_name_title,
            "name_first": self.random_first_name,
            "name_last": self.random_last_name,
            "age": self.random_age,
            "nat": self.random_nat,
        }
        param = random.choice(list(param_functions.keys()))  # Get random key
        return param, param_functions[param]()

    def random_update_param_table_contact_details_db(self):
        param_functions = {
            "phone": self.random_phone,
            "cell": self.random_cell,
        }
        param = random.choice(list(param_functions.keys()))  # Get random key
        return param, param_functions[param]()

    def random_update_param_table_media_data_db(self):  # Get random key
        return "picture", self.random_picture_url()

    def random_registration_data(self):
        param_functions = {
            "email": self.random_email,
            "username": self.random_username,
            "password": self.random_password,
            "password_md5": self.random_password_md5,
        }
        param = random.choice(list(param_functions.keys()))  # Get random key
        return param, param_functions[param]()

    def random_param_locations(self):
        param_functions = {
            "street_name": self.random_street_name,
            "street_number": self.random_street_number,
            "postcode": self.random_postcode,
            "latitude": self.random_latitude,
            "longitude": self.random_longitude,
        }
        param = random.choice(list(param_functions.keys()))  # Get random key
        return param, param_functions[param]()

    def random_param_cities(self):
        param_functions = {
            "city": self.random_city,
            "state": self.random_state,
            "country": self.random_country,
        }
        param = random.choice(list(param_functions.keys()))  # Get random key
        return param, param_functions[param]()

    @staticmethod
    def random_last_name():
        return "".join(random.choice(string.ascii_lowercase) for _ in range(10))

    @staticmethod
    def random_password_md5():
        random_string = secrets.token_hex(16)
        md5_hash = hashlib.md5(random_string.encode()).hexdigest()
        return md5_hash

    @staticmethod
    def random_picture_url() -> str:
        base_url = "https://example.com/images/"
        image_id = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        return f"{base_url}{image_id}.jpg"

    @staticmethod
    def random_first_name():
        return "".join(random.choice(string.ascii_lowercase) for _ in range(10))

    @staticmethod
    def random_city():
        return "".join(random.choice(string.ascii_lowercase) for _ in range(10))

    @staticmethod
    def random_state():
        return "".join(random.choice(string.ascii_uppercase) for _ in range(2))

    @staticmethod
    def random_country():
        countries = ["US", "CA", "MX", "UK", "FR", "DE", "ES", "IT", "JP", "KR", "RU"]
        return random.choice(countries)

    @staticmethod
    def random_street_name():
        return "".join(random.choice(string.ascii_lowercase) for _ in range(15))

    @staticmethod
    def random_nat() -> str:
        nationalities = ["US", "UK", "FR", "DE", "IN", "JP", "CN", "BR", "RU", "AU"]
        return random.choice(nationalities)

    @staticmethod
    def random_username():
        return "".join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(8)
        )

    @staticmethod
    def random_password():
        return "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(12)
        )

    def random_email(self):
        return (
            f"{self.random_first_name()}.{self.random_last_name()}@"
            f"{random.choice(['gmail', 'yahoo', 'hotmail'])}"
            f".com"
        )

    @staticmethod
    def random_phone():
        return (
            f"{random.randint(100, 999)}-"
            f"{random.randint(1000, 9999)}-"
            f"{random.randint(1000, 9999)}"
        )

    @staticmethod
    def random_cell():
        return (
            f"{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            f"-{random.randint(1000, 9999)}"
        )

    @staticmethod
    def random_age():
        return random.randint(18, 100)

    @staticmethod
    def random_number():
        return random.randint(18, 65)

    @staticmethod
    def random_postcode():
        return random.randint(1, 1000)

    @staticmethod
    def random_street_number():
        return random.randint(1, 10000)

    @staticmethod
    def random_name_title() -> str:
        titles = ["Mr.", "Mrs.", "Miss", "Ms.", "Dr.", "Prof."]
        return random.choice(titles)

    @staticmethod
    def random_latitude():
        return random.randint(10000, 99999)

    @staticmethod
    def random_longitude():
        return random.uniform(-180, 10)

    @staticmethod
    def random_gender() -> str:
        genders = ["Male", "Female"]
        return random.choice(genders)

    @pytest.mark.parametrize("param", [True, False])
    def test_get_users_db(self, param: bool, setting_te):
        result = get_users_db(setting_te, param)
        assert not isinstance(result, dict)

    @pytest.mark.parametrize('execution_number', range(1))
    def test_update_param_table_locations_db(self, execution_number,
                                             user_data_test, setting_te):

        email = user_data_test[0]
        print(email)
        param = self.random_param_locations()

        result = update_param_table_locations_db(
            setting_te, email, param[0], param[1]
        )
        assert not isinstance(result, list)

    @pytest.mark.parametrize('execution_number', range(20))
    def test_update_param_table_cities_db(self, execution_number, user_data_test, setting_te):
        email = user_data_test[0].email

        param = self.random_param_cities()
        result = update_param_table_cities_db(setting_te, email, param[0], [1])
        assert not isinstance(result, list)

    @pytest.mark.parametrize('execution_number', range(20))
    def test_update_param_table_registration_data_db(self, execution_number, user_data_test, setting_te):
        email = user_data_test[0].email
        param = self.random_registration_data()
        result = update_param_table_registration_data_db(
            setting_te, email, param[0], [1]
        )
        assert not isinstance(result, list)

    @pytest.mark.parametrize('execution_number', range(20))
    def test_update_param_table_media_data_db(self, execution_number, user_data_test, setting_te):
        email = user_data_test[0].email
        param = self.random_update_param_table_media_data_db()
        result = update_param_table_media_data_db(
            setting_te, email, param[0], [1]
        )
        assert not isinstance(result, list)

    @pytest.mark.parametrize('execution_number', range(20))
    def test_update_param_table_contact_details_db(self, execution_number, user_data_test, setting_te):
        email = user_data_test[0].email

        param = self.random_update_param_table_contact_details_db()
        result = update_param_table_contact_details_db(
            setting_te, email, param[0], [1]
        )
        assert not isinstance(result, list)

    @pytest.mark.parametrize('execution_number', range(20))
    def test_update_param_table_users_db(self, execution_number, user_data_test, setting_te):
        email = user_data_test[0].email

        param = self.random_update_param_table_users_db()
        result = update_param_table_users_db(
            setting_te, email, param[0], param[1]
        )
        assert not isinstance(result, list)
