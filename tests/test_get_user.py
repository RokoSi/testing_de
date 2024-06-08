import pytest

from settings import Settings
from src.db_use.get_user import get_valid_user


class testGetUser:
    @pytest.fixture
    def settings(self):
        return Settings(
            host="127.0.0.1",
            db="de_projects",
            user="admin",
            password="password",
            port=5432,
            url="https://randomuser.me/api/?password=special,upper,lower,number",
        )

    @pytest.mark.parametrize("param", [True, False])
    def test_get_valid_user(self, settings: Settings, param: bool):
        result = get_valid_user(settings, param)
        print(result)
        assert result is False
