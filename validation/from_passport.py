from datetime import date
from typing import Literal, Self
from pydantic import BaseModel, ConfigDict, Field, model_validator


class FromPassport(BaseModel):
    """
    Extracted fields from a scanned passport text.
    These fields represent key identity and document metadata typically found in machine-readable passports.
    """
    model_config = ConfigDict(validate_assignment=True, str_strip_whitespace=True)

    country: Optional[str] = None
    passport_number: Optional[str] = None
    surname: Optional[str] = None
    given_names: Optional[str] = None
    birth_date: Optional[str] = None # Simplified from date
    citizenship: Optional[str] = None
    sex: Optional[str] = None # Simplified from Literal
    issue_date: Optional[str] = None # Simplified from date
    expiry_date: Optional[str] = None # Simplified from date

    # --- Updated Validator ---
    # @model_validator(mode='after')
    # def check_expiry_date_after_issue_date(self) -> Self:
    #     # Only validate if both dates are present
    #     if self.issue_date is not None and self.expiry_date is not None:
    #         if self.issue_date >= self.expiry_date:
    #             # Raise error only if both dates are present and invalid
    #             raise ValueError(f'Expiry date ({self.expiry_date}) must be after issue date ({self.issue_date})')
    #     return self