from datetime import date
from validation.cross_validate import ExtractedData, xval_name_account_description
from validation.from_account import FromAccount
from validation.from_description import FromDescription
from validation.from_passport import FromPassport
from validation.from_profile import FromProfile


account_data = FromAccount(
    account_name="Astrid Janneke Willems",
    account_holder_name="Astrid Janneke",
    account_holder_surname="Willems",
    passport_number="HW8642009",
    reference_currency="EUR",
    other_currency=None,
    building_number="18",
    street_name="Lijnbaan",
    postal_code="7523 05",
    city="Assen",
    country="Netherlands",
    name="Astrid Janneke Willems",
    phone_number="+31 06 34579996",
    email="astrid.willems@upcmail.nl",
)

description_data = FromDescription(
    full_name="Astrid Janneke Willems",
    age=28,
    nationality="Netherlands",
    marital_status="single",
    has_children=False,
    secondary_education_school="Pieter Nieuwland College Utrecht",
    secondary_education_year=2016,
    university_name="Webster University Leiden",
    university_graduation_year=2020,
    occupation_title="Art Dealer",
    employer="Rijksmuseum Amsterdam",
    start_year=2021,
    annual_salary_eur=40000,
    total_savings_eur=20000,
    has_properties=False,
    inheritance_amount_eur=1590000,
    inheritance_year=2020,
    inheritance_source="grandmother (Oil and Gas Executive)",
)

passport_data = FromPassport(
    country="NLD",
    passport_number="HW8642009",
    surname="WILLEMS",
    given_names="ASTRID JANNEKE",
    birth_date=date(1997, 1, 19),
    citizenship="Austrian/ÖSTERREICH",
    sex="F",
    issue_date=date(2016, 6, 4),
    expiry_date=date(2026, 6, 3),
    signature_present=True,
    machine_readable_zone="P<NLDWILLEMS<<ASTRID<JANNEKE<<<<<<<<<<<<<<<<<<<HW8642009NLD970119",
)

profile_data = FromProfile(
    first_name="Astrid Janneke",
    last_name="Willems",
    date_of_birth=date(1997, 1, 19),
    nationality="Dutch",
    country_of_domicile="Netherlands",
    gender="Female",
    passport_number="HW8642009",
    id_type="passport",
    id_issue_date=date(2016, 6, 4),
    id_expiry_date=date(2026, 6, 3),
    phone="+31 06 34579996",
    email="astrid.willems@upcmail.nl",
    address="Lijnbaan 18, 7523 05 Assen",
    politically_exposed_person=False,
    marital_status="Single",
    highest_education="Tertiary",
    education_history="Webster University Leiden (2020)",
    employment_status="Employee",
    employment_since=2021,
    employer="Rijksmuseum Amsterdam",
    position="Art Dealer",
    annual_salary_eur=40000.0,
    total_wealth_range="1.5m-5m",
    origin_of_wealth=["Employment", "Inheritance"],
    inheritance_details="Grandmother, 2020, Oil and Gas Executive",
    business_assets_eur=20000.0,
    estimated_annual_income="<250k",
    income_country="Netherlands",
    commercial_account=False,
    investment_risk_profile="High",
    mandate_type="Advisory",
    investment_experience="Experienced",
    investment_horizon="Medium",
    preferred_markets=["Denmark", "Netherlands"],
    total_aum=1610000.0,
    aum_to_transfer=1320200.0,
)


def test_xval_name_account_description() -> None:
    data = ExtractedData(
        account=account_data,
        description=description_data,
        passport=passport_data,
        profile=profile_data,
    )

    failure = xval_name_account_description(data)
    assert failure is None
