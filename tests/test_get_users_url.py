import pytest


from src.json_parsing.get_user import get_users_url
from src.settings import Settings


class TestGetUserURL:
    @pytest.fixture
    def settings(self):
        return Settings(url="https://randomuser.me/api/?results=")

    @pytest.mark.parametrize("count_users", ["_", "z", "uf2"])
    def test_get_users_url_negative(self, count_users: int, settings: Settings):
        try:
            result = get_users_url(int(count_users), settings)
            assert bool(result) is False
        except ValueError:
            assert False is False

    @pytest.mark.parametrize("count_users", [1, 10, 20, 30])
    def test_get_users_url_positive(self, count_users: int, settings: Settings):
        result = get_users_url(count_users, settings)
        assert bool(result) is True
