from typing import Optional # Keep Optional, remove others
from pydantic import BaseModel, ConfigDict # Removed Field


class FromProfile(BaseModel):
    """
    Fields which can be extracted from description.txt - All fields optional and simplified to string where possible.
    """
    model_config = ConfigDict(validate_assignment=True, str_strip_whitespace=True) # Keep config if needed

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None # Simplified from date
    nationality: Optional[str] = None
    country_of_domicile: Optional[str] = None
    gender: Optional[str] = None # Simplified from Literal

    # ID information
    passport_number: Optional[str] = None # Simplified, removed Field constraints
    id_type: Optional[str] = None # Simplified from Literal
    id_issue_date: Optional[str] = None # Simplified from date
    id_expiry_date: Optional[str] = None # Simplified from date

    # Contact
    phone: Optional[str] = None # Simplified, removed Field constraints
    email: Optional[str] = None # Simplified, removed Field constraints
    address: Optional[str] = None

    # Personal info
    politically_exposed_person: Optional[str] = None # Simplified from bool
    marital_status: Optional[str] = None # Simplified from Literal
    highest_education: Optional[str] = None # Simplified from Literal
    education_history: Optional[str] = None

    # Employment
    employment_status: Optional[str] = None # Simplified from Literal
    employment_since: Optional[str] = None # Simplified from int
    employer: Optional[str] = None
    position: Optional[str] = None
    annual_salary_eur: Optional[str] = None # Simplified from float

    # Wealth background
    total_wealth_range: Optional[str] = None # Simplified from Literal
    # List types are often handled differently; simplifying to a single string might lose info.
    # Keeping as Optional[str] based on request, but consider if Optional[List[str]] = None is better long-term.
    origin_of_wealth: Optional[str] = None # Simplified from List[Literal]
    inheritance_details: Optional[str] = None

    # Assets
    business_assets_eur: Optional[str] = None # Simplified from float, removed Field constraint

    # Income
    estimated_annual_income: Optional[str] = None # Was already Optional[str]
    income_country: Optional[str] = None

    # Account preferences
    commercial_account: Optional[str] = None # Simplified from bool
    investment_risk_profile: Optional[str] = None # Simplified from Literal
    mandate_type: Optional[str] = None # Simplified from Literal
    investment_experience: Optional[str] = None # Simplified from Literal
    investment_horizon: Optional[str] = None # Simplified from Literal
     # Keeping as Optional[str] based on request, but consider if Optional[List[str]] = None is better long-term.
    preferred_markets: Optional[str] = None # Simplified from List[str]

    # Assets under management
    total_aum: Optional[str] = None # Simplified from float
    aum_to_transfer: Optional[str] = None # Simplified from float