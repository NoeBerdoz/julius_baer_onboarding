from datetime import date

from pydantic import ValidationError
import pytest
from tests.dummy import dummy_account, dummy_passport
from validation.from_passport import FromPassport


def test_check_expiry_date_after_issue_date() -> None:
    dummy = dummy_passport()
    with pytest.raises(ValidationError):
        dummy.expiry_date = date(1900, 1, 1)

def test_invalid_email() -> None:
    dummy = dummy_account()
    with pytest.raises(ValidationError):
        dummy.email = "this is not a valid email account"

def test_invalid_phone_number() -> None:
    dummy = dummy_account()
    with pytest.raises(ValidationError):
        dummy.phone_number = "This should be invalid"
    dummy.phone_number = "+41 32 333 33 33"