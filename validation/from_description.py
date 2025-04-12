from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class FromDescription(BaseModel):
    """
    Fields which can be extracted from description.txt
    """
    model_config = ConfigDict(validate_assignment=True, str_strip_whitespace=True)

    
    full_name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0, le=120)
    nationality: str = Field(..., min_length=1)

    marital_status: Literal["single", "married", "divorced", "widowed"]
    has_children: bool

    secondary_education_school: str
    secondary_education_year: int = Field(..., ge=1900, le=2100)
    university_name: str
    university_graduation_year: int = Field(..., ge=1900, le=2100)

    occupation_title: str
    employer: str
    start_year: int = Field(..., ge=1900, le=2100)
    annual_salary_eur: float = Field(..., ge=0)

    total_savings_eur: float = Field(..., ge=0)
    has_properties: bool

    inheritance_amount_eur: float = Field(..., ge=0)
    inheritance_year: int = Field(..., ge=1900, le=2100)
    inheritance_source: str

