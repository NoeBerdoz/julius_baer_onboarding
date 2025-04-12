from typing import Literal, Optional, Self
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

class FromAccount(BaseModel):
    """
    Fields which can be extracted from account.pdf
    """
    model_config = ConfigDict(validate_assignment=True, str_strip_whitespace=True)

    # Details of the Account and Client
    account_name: str = Field(min_length=1)
    account_holder_name: str = Field(min_length=1)
    account_holder_surname: str = Field(min_length=1)

    @model_validator(mode='after')
    def check_account_name_is_name_surname(self) -> Self:
        combined = f"{self.account_holder_name} {self.account_holder_surname}"
        if combined != self.account_name:
            raise ValueError(f'Account name is not name + surname: {self.account_name} != {combined}')
        return self

    passport_number: str = Field(min_length=5)

    reference_currency: Literal["CHF", "EUR", "USD", "Other"]
    other_currency: Optional[str] = None

    # Delivery of Communication
    building_number: str = Field(min_length=1)
    street_name: str = Field(min_length=1)
    postal_code: str = Field(min_length=1)
    city: str = Field(min_length=1)
    country: str = Field(min_length=1)

    # Application for e-banking
    ebanking_name: str = Field(min_length=1)
    @model_validator(mode='after')
    def check_account_name_ebanking_name(self) -> Self:
        if self.ebanking_name != self.account_name:
            raise ValueError(f'Ebanking name is different from account name')
        return self
    phone_number: str = Field(..., min_length=8)
    email: str = Field(min_length=5)