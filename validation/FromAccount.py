from typing import Literal, Optional, Self
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class FromAccount(BaseModel):
    """
    Fields which can be extracted from account.pdf
    """
    model_config = ConfigDict(validate_assignment=True, str_strip_whitespace=True)

    # From account.pdf
    account_name: str = Field(..., min_length=1)
    account_holder_name: str = Field(..., min_length=1)
    account_holder_surname: str = Field(..., min_length=1)

    @model_validator(mode='after')
    def check_account_name_is_name_surname(self) -> Self:
        combined = f"{self.account_holder_name} {self.account_holder_surname}"
        if combined != self.account_name:
            raise ValueError(f'Account name is not name + surname: {self.account_name} != {combined}')
        return self

    passport_number: str = Field(..., min_length=5)

    reference_currency: Literal["CHF", "EUR", "USD", "Other"]
    other_currency: Optional[str] = None

    building_number: str = Field(..., min_length=1)
    street_name: str = Field(..., min_length=1)
    postal_code: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)

    name: str = Field(..., min_length=1)
    phone_number: str = Field(..., min_length=6)
    email: EmailStr