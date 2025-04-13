from typing import Optional # Removed Literal, Self
from pydantic import BaseModel, ConfigDict # Removed Field, model_validator
# Removed PhoneNumber import as it's not used and types are simplified

class FromAccount(BaseModel):
    """
    Fields which can be extracted from account.pdf - All fields optional and simplified to string.
    Validators removed for testing purposes.
    """
    model_config = ConfigDict(validate_assignment=True, str_strip_whitespace=True)

    # Details of the Account and Client
    account_name: Optional[str] = None
    account_holder_name: Optional[str] = None
    account_holder_surname: Optional[str] = None

    # --- Updated Validator 1 ---
    # @model_validator(mode='after')
    # def check_account_name_is_name_surname(self) -> Self:
    #     # Only validate if all relevant fields are present
    #     if self.account_holder_name is not None and \
    #        self.account_holder_surname is not None and \
    #        self.account_name is not None:
    #         combined = f"{self.account_holder_name} {self.account_holder_surname}"
    #         if combined != self.account_name:
    #             raise ValueError(f'Account name is not name + surname: {self.account_name} != {combined}')
    #     return self

    passport_number: Optional[str] = None  # Removed Field constraint

    reference_currency: Optional[str] = None  # Simplified from Literal
    other_currency: Optional[str] = None

    # Delivery of Communication
    building_number: Optional[str] = None
    street_name: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

    # Application for e-banking
    ebanking_name: Optional[str] = None

    # --- Updated Validator 2 ---
    # @model_validator(mode='after')
    # def check_account_name_ebanking_name(self) -> Self:
    #      # Only validate if both fields are present
    #     if self.ebanking_name is not None and self.account_name is not None:
    #         if self.ebanking_name != self.account_name:
    #             raise ValueError(f'Ebanking name ({self.ebanking_name}) is different from account name ({self.account_name})')
    #     return self

    # Kept as Optional[str], but you might consider Optional[PhoneNumber]
    # if you want specific phone number validation using pydantic-extra-types
    phone_number: Optional[str] = None  # Removed Field constraint
    email: Optional[str] = None  # Removed Field constraint