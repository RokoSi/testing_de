import pytest
import random
import string
import hashlib
import secrets

from src.DataProvider.DataProviderDB import get_users_db, get_check_email, update_param_table_locations_db, save_user, \
    update_param_table_cities_db, update_param_table_registration_data_db, update_param_table_media_data_db, \
    update_param_table_contact_details_db, update_param_table_users_db


class TestDataProviderDB:

    def random_update_param_table_users_db(self):
        param_functions = {
            'gender': self.random_gender,
            'name_title': self.random_name_title,
            'name_first': self.random_first_name,
            'name_last': self.random_last_name,
            'age': self.random_age,
            'nat': self.random_nat
        }
        param = random.choice(list(param_functions.keys()))  # Get random key
        return param, param_functions[param]()

    def random_update_param_table_contact_details_db(self):
        param_functions = {
            'phone': self.random_phone,
            'cell': self.random_cell,
        }
        param = random.choice(list(param_functions.keys()))  # Get random key
        return param, param_functions[param]()

    def random_update_param_table_media_data_db(self):  # Get random key
        return "picture", self.random_picture_url()

    def random_registration_data(self):
        param_functions = {
            'email': self.random_email,
            'username': self.random_username,
            'password': self.random_password,
            'password_md5': self.random_password_md5,
        }
        param = random.choice(list(param_functions.keys()))  # Get random key
        return param, param_functions[param]()

    def random_param_locations(self):
        param_functions = {
            'street_name': self.random_street_name,
            'street_number': self.random_street_number,
            'postcode': self.random_postcode,
            'latitude': self.random_latitude,
            'longitude': self.random_longitude,
        }
        param = random.choice(list(param_functions.keys()))  # Get random key
        return param, param_functions[param]()

    def random_param_cities(self):
        param_functions = {
            'city': self.random_city,
            'state': self.random_state,
            'country': self.random_country
        }
        param = random.choice(list(param_functions.keys()))  # Get random key
        return param, param_functions[param]()

    @staticmethod
    def random_last_name():
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(10))

    @staticmethod
    def random_password_md5():
        random_string = secrets.token_hex(16)
        md5_hash = hashlib.md5(random_string.encode()).hexdigest()
        return md5_hash

    @staticmethod
    def random_picture_url() -> str:
        base_url = "https://example.com/images/"
        image_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return f"{base_url}{image_id}.jpg"

    @staticmethod
    def random_first_name():
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(10))

    @staticmethod
    def random_city():
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(10))

    @staticmethod
    def random_state():
        return ''.join(random.choice(string.ascii_uppercase) for _ in range(2))

    @staticmethod
    def random_country():
        countries = ["US", "CA", "MX", "UK", "FR", "DE", "ES", "IT", "JP", "KR", "RU"]
        return random.choice(countries)

    @staticmethod
    def random_street_name():
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(15))

    @staticmethod
    def random_nat() -> str:
        nationalities = ["US", "UK", "FR", "DE", "IN", "JP", "CN", "BR", "RU", "AU"]
        return random.choice(nationalities)

    @staticmethod
    def random_username():
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))

    @staticmethod
    def random_password():
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))

    def random_email(self):
        return f"{self.random_first_name()}.{self.random_last_name()}@{random.choice(['gmail',
                                                                                      'yahoo', 'hotmail'])}.com"

    @staticmethod
    def random_phone():
        return f"{random.randint(100, 999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"

    @staticmethod
    def random_cell():
        return f"{random.randint(100, 999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"

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
    def test_get_users_db(self, param: bool):
        result = get_users_db(param)
        result: bool = type(result) is dict
        assert result is False

    @pytest.mark.parametrize("email",
                             ["simon.gill@example.com", "javier.george@example.com", "dinand.holwerda"
                                                                                     "@example.com",
                              "jiry.beunk@example.com"])
    def test_get_check_email_positive(self, email: str):
        result = get_check_email(email)

        result: bool = type(result) is list
        assert result is True

    @pytest.mark.parametrize("email", ["asdasfcasd", "qedqfq", "plainaddress", "@missingusername.com", "username"
                                                                                                       "@.com.my",
                                       "username@com..com", "username@domain@domain.com"])
    def test_get_check_email_negative(self, email: str):
        result = get_check_email(email)
        result: bool = type(result) is list
        assert result is False

    def test_update_param_table_locations_db(self):
        save_user((("Kurikka", "Kymenlaakso", "Finland"), ('female', "Mrs", "Emilia", "last", "43", "FI"),
                   ("9-335-580", "043-987-16-00"), "https://randomuser.me/api/portraits/women/20.jpg",
                   ("emilia.salonen@example.com", "organicduck241", "veritas", "9d39d4c23e7a09002e88aad44a3fbaff"),
                   ("Mechelininkatu", "8736", "90508", "-24.5426", "123.6395")))
        param = self.random_param_locations()

        result = update_param_table_locations_db("emilia.salonen@example.com", param[0], param[1])
        result: bool = type(result) is list
        print(param)
        assert result is False

    def test_update_param_table_cities_db(self):
        save_user((("Kurikka", "Kymenlaakso", "Finland"), ('female', "Mrs", "Emilia", "last", "43", "FI"),
                   ("9-335-580", "043-987-16-00"), "https://randomuser.me/api/portraits/women/20.jpg",
                   ("emilia.salonen@example.com", "organicduck241", "veritas", "9d39d4c23e7a09002e88aad44a3fbaff"),
                   ("Mechelininkatu", "8736", "90508", "-24.5426", "123.6395")))
        param = self.random_param_cities()
        result = update_param_table_cities_db("emilia.salonen@example.com", param[0], [1])
        result: bool = type(result) is list
        print(param)
        assert result is False

    def test_update_param_table_registration_data_db(self):
        save_user((("Kurikka", "Kymenlaakso", "Finland"), ('female', "Mrs", "Emilia", "last", "43", "FI"),
                   ("9-335-580", "043-987-16-00"), "https://randomuser.me/api/portraits/women/20.jpg",
                   ("emilia.salonen@example.com", "organicduck241", "veritas", "9d39d4c23e7a09002e88aad44a3fbaff"),
                   ("Mechelininkatu", "8736", "90508", "-24.5426", "123.6395")))
        param = self.random_registration_data()
        result = update_param_table_registration_data_db("emilia.salonen@example.com", param[0], [1])
        result: bool = type(result) is list
        print(param)
        assert result is False

    def test_update_param_table_media_data_db(self):
        save_user((("Kurikka", "Kymenlaakso", "Finland"), ('female', "Mrs", "Emilia", "last", "43", "FI"),
                   ("9-335-580", "043-987-16-00"), "https://randomuser.me/api/portraits/women/20.jpg",
                   ("emilia.salonen@example.com", "organicduck241", "veritas", "9d39d4c23e7a09002e88aad44a3fbaff"),
                   ("Mechelininkatu", "8736", "90508", "-24.5426", "123.6395")))
        param = self.random_update_param_table_media_data_db()
        result = update_param_table_media_data_db("emilia.salonen@example.com", param[0], [1])
        result: bool = type(result) is list
        print(param)
        assert result is False

    def test_update_param_table_contact_details_db(self):
        save_user((("Kurikka", "Kymenlaakso", "Finland"), ('female', "Mrs", "Emilia", "last", "43", "FI"),
                   ("9-335-580", "043-987-16-00"), "https://randomuser.me/api/portraits/women/20.jpg",
                   ("emilia.salonen@example.com", "organicduck241", "veritas", "9d39d4c23e7a09002e88aad44a3fbaff"),
                   ("Mechelininkatu", "8736", "90508", "-24.5426", "123.6395")))
        param = self.random_update_param_table_contact_details_db()
        result = update_param_table_contact_details_db("emilia.salonen@example.com", param[0], [1])
        result: bool = type(result) is list
        print(param)
        assert result is False

    def test_update_param_table_users_db(self):
        save_user((("Kurikka", "Kymenlaakso", "Finland"), ('female', "Mrs", "Emilia", "last", "43", "FI"),
                   ("9-335-580", "043-987-16-00"), "https://randomuser.me/api/portraits/women/20.jpg",
                   ("emilia.salonen@example.com", "organicduck241", "veritas", "9d39d4c23e7a09002e88aad44a3fbaff"),
                   ("Mechelininkatu", "8736", "90508", "-24.5426", "123.6395")))
        param = self.random_update_param_table_users_db()
        result = update_param_table_users_db("emilia.salonen@example.com", param[0], [1])
        result: bool = type(result) is list
        print(param)
        assert result is False
