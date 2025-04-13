from typing import Optional # Removed Literal
from pydantic import BaseModel, ConfigDict # Removed Field


class FromDescription(BaseModel):
    """
    Fields which can be extracted from description.txt - All fields optional and simplified to string.
    """
    model_config = ConfigDict(validate_assignment=True, str_strip_whitespace=True)

    full_name: Optional[str] = None
    age: Optional[str] = None # Simplified from int
    nationality: Optional[str] = None
    marital_status: Optional[str] = None # Simplified from Literal
    has_children: Optional[str] = None # Simplified from bool

    secondary_education_school: Optional[str] = None
    secondary_education_year: Optional[str] = None # Simplified from int
    university_name: Optional[str] = None
    university_graduation_year: Optional[str] = None # Simplified from int

    occupation_title: Optional[str] = None
    employer: Optional[str] = None
    start_year: Optional[str] = None # Simplified from int
    annual_salary_eur: Optional[str] = None # Simplified from float

    total_savings_eur: Optional[str] = None # Simplified from float
    has_properties: Optional[str] = None # Simplified from bool

    inheritance_amount_eur: Optional[str] = None # Simplified from float
    inheritance_year: Optional[str] = None # Simplified from int
    inheritance_source: Optional[str] = None