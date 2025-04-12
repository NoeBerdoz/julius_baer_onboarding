from tests.dummy import dummy_data
from validation.cross_validate import xval_all, xval_email_account_profile, xval_name_account_description



def test_xval_name_account_description() -> None:
    failure = xval_name_account_description(dummy_data())
    assert failure is None

def test_xval_email_account_profile() -> None:
    failure = xval_email_account_profile(dummy_data()) 
    assert failure is None

def test_xval_all() -> None:
    failures = xval_all(dummy_data())
    assert len(failures) == 0