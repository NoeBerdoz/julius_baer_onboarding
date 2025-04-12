from datetime import date

from pydantic import ValidationError
import pytest
from tests.dummy import dummy_passport
from validation.from_passport import FromPassport


def test_check_expiry_date_after_issue_date() -> None:
    dummy = dummy_passport()
    with pytest.raises(ValidationError):
        dummy.expiry_date = date(1900, 1, 1)