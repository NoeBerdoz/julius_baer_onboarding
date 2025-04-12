from enum import StrEnum
from typing import Any, Callable, Optional
from pydantic import BaseModel

from validation import FromAccount, FromDescription, FromPassport, FromProfile


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
    if data.account.account_holder_name != data.description.full_name:
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


def xref_all(data: ExtractedData) -> list[XValFailure]:
    xref_validators: list[Callable[[ExtractedData], Optional[XValFailure]]] = [
        xval_name_account_description
    ]

    validation_failures = []
    for validator in xref_validators:
        failure = validator(data)
        if not failure is None:
            validation_failures.append(failure)
    return validation_failures
