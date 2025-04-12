from datetime import date
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class FromPassport(BaseModel):
    """
    Fields which can be extracted from description.txt
    """
    model_config = ConfigDict(validate_assignment=True, str_strip_whitespace=True)
    
    country: str = Field(..., min_length=3, max_length=3)  # ISO 3166-1 alpha-3
    passport_number: str = Field(..., min_length=9, max_length=9, pattern=r"^[A-Z0-9]{9}$")

    surname: str = Field(..., min_length=1)
    given_names: str = Field(..., min_length=1)

    birth_date: date
    citizenship: str = Field(..., min_length=2)
    sex: Literal["M", "F"]

    issue_date: date
    expiry_date: date

    signature_present: bool

    machine_readable_zone: str = Field(..., min_length=44)