import pytest

from src.validators.validator_email import validator_email


class TestValidatorEmail:
    @pytest.mark.parametrize(
        "email",
        [
            "john.doe@example.com",
            "jane_doe123@subdomain.example.co.uk",
            "user.name+tag+sorting@example.com",
            "x@example.io",
            "niceandsimple@example.com",
        ],
    )
    def test_validator_email_positive(self, email):
        assert validator_email(email) is True

    @pytest.mark.parametrize(
        "email",
        [
            "plainaddress",
            "@missingusername.com",
            "username@.com.my",
            "username@com..com",
            "username@domain@domain.com",
        ],
    )
    def test_validator_email_negative(self, email):
        assert validator_email(email) is False
