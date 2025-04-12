from enum import StrEnum
from typing import Any, Callable
from pydantic import BaseModel

from validation import FromAccount, FromDescription, FromPassport, FromProfile



class ValidatedData(BaseModel):
    account: FromAccount
    description: FromDescription
    passport: FromPassport
    profile: FromProfile

class DocType(StrEnum):
    account = "account"
    description = "description"
    passport = "passport"
    profile = "profile"


class ValidationFailure(BaseModel):
    doc1_type: DocType
    doc1_val: str

    doc2_type: DocType
    doc2_val: str



def xref_client_name(data: ValidatedData) -> ValidationFailure:
    if data.account.account_holder_name != data.description.full_name:
        return ValidationFailure(
            doc1_type=DocType.account, doc1_val=f"{data.account.account_holder_name=}",
            doc2_type=DocType.description, doc2_val=f"{data.description.full_name=}"
        )
    # TODO CONTINUE

def xref_all(data: ValidatedData) -> list[ValidationFailure]:
    xref_validators: list[Callable[[ValidatedData], ValidationFailure]] = [xref_client_name]

    validation_failures = []
    for validator in xref_validators:
        validation_failures.append(validator(data))
    return validation_failures