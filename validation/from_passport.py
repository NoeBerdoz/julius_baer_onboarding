from datetime import date
from typing import Literal, Self
from pydantic import BaseModel, ConfigDict, Field, model_validator


class FromPassport(BaseModel):
    """
    Extracted fields from a scanned passport text.
    These fields represent key identity and document metadata typically found in machine-readable passports.
    """
    model_config = ConfigDict(validate_assignment=True, str_strip_whitespace=True)

    country: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="The country issuing the passport, as a 3-letter ISO 3166-1 alpha-3 code (e.g., 'CHE' for Switzerland)."
    )

    passport_number: str = Field(
        ...,
        min_length=9,
        max_length=9,
        pattern=r"^[A-Z0-9]{9}$",
        description="The passport number, exactly 9 alphanumeric uppercase characters."
    )

    surname: str = Field(
        ...,
        min_length=1,
        description="The surname (family name) of the passport holder."
    )

    given_names: str = Field(
        ...,
        min_length=1,
        description="The given names (first and middle names) of the passport holder."
    )

    @model_validator(mode='after')
    def check_expiry_date_after_issue_date(self) -> Self:
        if self.issue_date >= self.expiry_date:
            raise ValueError(f'Expiry date is not after issue date')
        return self

    birth_date: date = Field(
        ...,
        description="Date of birth of the passport holder in ISO format (YYYY-MM-DD)."
    )

    citizenship: str = Field(
        ...,
        min_length=2,
        description="The nationality or citizenship of the passport holder, preferably as a country name or ISO code."
    )

    sex: Literal["M", "F"] = Field(
        ...,
        description="Sex of the passport holder: 'M' for male, 'F' for female."
    )

    issue_date: date = Field(
        ...,
        description="Date when the passport was issued, in ISO format (YYYY-MM-DD)."
    )

    expiry_date: date = Field(
        ...,
        description="Date when the passport expires, in ISO format (YYYY-MM-DD)."
    )