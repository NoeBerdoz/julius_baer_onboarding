from services.extractor import extract_passport
from tests.dummy import dummy_client_data


def test_extract_passport() -> None:
    client_data = dummy_client_data()[0]
    passport = extract_passport(client_data)
    passport