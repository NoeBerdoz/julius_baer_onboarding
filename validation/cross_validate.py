from datetime import date, timedelta
from enum import StrEnum
from typing import Any, Callable, Optional
from pydantic import BaseModel

from validation.from_account import FromAccount
from validation.from_description import FromDescription
from validation.from_passport import FromPassport
from validation.from_profile import FromProfile



class ExtractedData(BaseModel):
    account: FromAccount
    description: FromDescription
    passport: FromPassport
    profile: FromProfile


class DocType(StrEnum):
    account = "account"
    description = "description"
    passport = "passport"
    profile = "profile"


class XValFailure(BaseModel):
    doc1_type: DocType
    doc1_val: str

    doc2_type: DocType
    doc2_val: str


def xval_name_account_description(data: ExtractedData) -> Optional[XValFailure]:
    if data.account.account_name != data.description.full_name:
        return XValFailure(
            doc1_type=DocType.account,
            doc1_val=f"{data.account.account_holder_name=}",
            doc2_type=DocType.description,
            doc2_val=f"{data.description.full_name=}",
        )


def xval_email_account_profile(data: ExtractedData) -> Optional[XValFailure]:
    if data.account.email != data.profile.email:
        return XValFailure(
            doc1_type=DocType.account,
            doc1_val=f"{data.account.email=}",
            doc2_type=DocType.profile,
            doc2_val=f"{data.profile.email=}"
        )

def xval_passport_no_account_passport(data: ExtractedData) -> Optional[XValFailure]:
    if data.account.passport_number != data.passport.passport_number:
        return XValFailure(
            doc1_type=DocType.account,
            doc1_val=f"{data.account.passport_number=}",
            doc2_type=DocType.passport,
            doc2_val=f"{data.passport.passport_number=}"
        )

def birth_date_to_age(birth_date: date) -> int:
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def xval_age_description_passport(data: ExtractedData) -> Optional[XValFailure]:
    age_from_birth_date = birth_date_to_age(data.passport.birth_date)
    if data.description.age != age_from_birth_date:
        return XValFailure(
            doc1_type=DocType.description,
            doc1_val=f"{data.description.age=}",
            doc2_type=DocType.passport,
            doc2_val=f"{data.passport.birth_date=}"
        )

def xval_all(data: ExtractedData) -> list[XValFailure]:
    xref_validators: list[Callable[[ExtractedData], Optional[XValFailure]]] = [
        xval_name_account_description,
        xval_email_account_profile,
        xval_passport_no_account_passport,
        xval_age_description_passport
    ]

    validation_failures = []
    for validator in xref_validators:
        failure = validator(data)
        if not failure is None:
            validation_failures.append(failure)
    return validation_failures
