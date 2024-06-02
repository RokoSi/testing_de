import pytest

from src.DataProvider.DataProviderURl import get_users_url


class TestDataProviderURL:
    @pytest.mark.parametrize("count_user , url", [("fda", "h!ttps://ya.ru/?npr="), ("2", "h!ttps://ya.ru/?npr=")])
    def test_get_users_url_negative(self, count_user: int, url: str):
        result = get_users_url(count_user, url)
        assert result is False

    @pytest.mark.parametrize("count_user , url", [("1", "https://randomuser.me/api/?results="), ("2", "https"
                                                                                                      "://randomuser"
                                                                                                      ".me/api"
                                                                                                      "/?results=")])
    def test_get_users_url_positive(self, count_user: int, url: str):
        result = get_users_url(count_user, url)
        result: bool = type(result) is dict
        assert result is True
