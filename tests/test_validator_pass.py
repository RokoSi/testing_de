import pytest

from src.validators.validator_password import validator_pass


class TestValidatorPassword:
    @pytest.mark.parametrize(
        "password",
        [
            "1234aD@.",
            "1234aD@",
            "1234aD@!",
            "GoodPass123!",
            "Pa$$w0rd",
            "P@ssw0rd123",
            'GoodPass123"',
            "CorrectHorseBatteryStaple1!",
        ],
    )
    def test_validator_password_positive(self, password):
        assert validator_pass(password) is True

    @pytest.mark.parametrize(
        "password",
        [
            "1234",
            "1234a",
            "1234aD",
            "1234aadGGD",
            "PASSWORD123",
            "Password",
            "12345678",
            "NoSpecialChar1",
        ],
    )
    def test_validator_password_negative(self, password):
        assert validator_pass(password) is False
