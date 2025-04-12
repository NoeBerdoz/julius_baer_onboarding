from datetime import date
from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class FromProfile(BaseModel):
    """
    Fields which can be extracted from description.txt
    """
    model_config = ConfigDict(validate_assignment=True, str_strip_whitespace=True)

    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    date_of_birth: date
    nationality: str
    country_of_domicile: str
    gender: Literal["Female", "Male"]

    # ID information
    passport_number: str = Field(..., min_length=9, max_length=9, regex=r"^[A-Z0-9]{9}$")
    id_type: Literal["passport"]
    id_issue_date: date
    id_expiry_date: date

    # Contact
    phone: str = Field(..., min_length=8)
    email: EmailStr
    address: str

    # Personal info
    politically_exposed_person: bool
    marital_status: Literal["Single", "Married", "Divorced", "Widowed"]
    highest_education: Literal["Tertiary", "Secondary", "Primary", "None"]
    education_history: Optional[str] = None

    # Employment
    employment_status: Literal["Employee", "Self-Employed", "Unemployed", "Retired", "Student", "Diplomat", "Military", "Homemaker", "Other"]
    employment_since: Optional[int] = None
    employer: Optional[str] = None
    position: Optional[str] = None
    annual_salary_eur: Optional[float] = None

    # Wealth background
    total_wealth_range: Literal["<1.5m", "1.5m-5m", "5m-10m", "10m-20m", "20m-50m", ">50m"]
    origin_of_wealth: List[Literal["Employment", "Inheritance", "Business", "Investments", "Sale of real estate", "Retirement package", "Other"]]
    inheritance_details: Optional[str] = None

    # Assets
    business_assets_eur: float = Field(..., ge=0)

    # Income
    estimated_annual_income: Literal["<250k", "250k-500k", "500k-1m", ">1m"]
    income_country: str

    # Account preferences
    commercial_account: bool
    investment_risk_profile: Literal["Low", "Moderate", "Considerable", "High"]
    mandate_type: Literal["Advisory", "Discretionary"]
    investment_experience: Literal["Inexperienced", "Experienced", "Expert"]
    investment_horizon: Literal["Short", "Medium", "Long-Term"]
    preferred_markets: List[str]

    # Assets under management
    total_aum: float
    aum_to_transfer: float