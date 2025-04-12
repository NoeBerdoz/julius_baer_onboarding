from tests.dummy import dummy_client_data
from utils.parsers.passport_parser import process_passport


def test_passport_parser() -> None:
    client_data = dummy_client_data()[0]

    passport = process_passport(client_data.get("passport"))
    passport