from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class JobType(Enum):
    FULL_TIME = ("fulltime",)
    PART_TIME = "parttime"
    CONTRACT = ("contract", "contractor")
    TEMPORARY = ("temporary",)
    INTERNSHIP = ("internship",)
    NIGHTS = ("nights",)
    OTHER = ("other",)
    SUMMER = ("summer",)
    VOLUNTEER = ("volunteer",)


class Country(Enum):
    """
    Gets the subdomain for Indeed and Glassdoor.
    The second item in the tuple is the subdomain (and API country code if there's a ':' separator) for Indeed
    """

    CANADA = ("canada", "ca", "ca")
    CHILE = ("chile", "cl")
    COLOMBIA = ("colombia", "co")
    INDIA = ("india", "in", "co.in")
    PERU = ("peru", "pe")
    VENEZUELA = ("venezuela", "ve")
    VIETNAM = ("vietnam", "vn", "com")
    USA = ("usa,us,united states", "www:us", "com")

    # internal for ziprecruiter
    US_CANADA = ("usa/ca", "www")

    # internal for linkedin
    WORLDWIDE = ("worldwide", "www")

    @property
    def indeed_domain_value(self):
        subdomain, _, api_country_code = self.value[1].partition(":")
        if subdomain and api_country_code:
            return subdomain, api_country_code.upper()
        return self.value[1], self.value[1].upper()

    @classmethod
    def from_string(cls, country_str: str):
        """Convert a string to the corresponding Country enum."""
        country_str = country_str.strip().lower()
        for country in cls:
            country_names = country.value[0].split(",")
            if country_str in country_names:
                return country
        valid_countries = [country.value for country in cls]
        raise ValueError(
            f"Invalid country string: '{country_str}'. Valid countries are: {', '.join([country[0] for country in valid_countries])}"
        )


class Location(BaseModel):
    country: Country | str | None = None
    city: Optional[str] = None
    state: Optional[str] = None

    def display_location(self) -> str:
        location_parts = []
        if self.city:
            location_parts.append(self.city)
        if self.state:
            location_parts.append(self.state)
        if isinstance(self.country, str):
            location_parts.append(self.country)
        elif self.country and self.country not in (
            Country.US_CANADA,
            Country.WORLDWIDE,
        ):
            country_name = self.country.value[0]
            if "," in country_name:
                country_name = country_name.split(",")[0]
            if country_name in ("usa", "uk"):
                location_parts.append(country_name.upper())
            else:
                location_parts.append(country_name.title())
        return ", ".join(location_parts)


class CompensationInterval(Enum):
    YEARLY = "yearly"
    MONTHLY = "monthly"
    WEEKLY = "weekly"
    DAILY = "daily"
    HOURLY = "hourly"

    @classmethod
    def get_interval(cls, pay_period):
        interval_mapping = {
            "YEAR": cls.YEARLY,
            "HOUR": cls.HOURLY,
        }
        if pay_period in interval_mapping:
            return interval_mapping[pay_period].value
        else:
            return cls[pay_period].value if pay_period in cls.__members__ else None


class Compensation(BaseModel):
    interval: Optional[CompensationInterval] = None
    min_amount: float | None = None
    max_amount: float | None = None
    currency: Optional[str] = "USD"


class DescriptionFormat(Enum):
    MARKDOWN = "markdown"
    HTML = "html"


class JobPost(BaseModel):
    title: str
    company_name: str | None
    job_url: str
    job_url_direct: str | None = None
    location: Optional[Location]

    description: str | None = None
    company_url: str | None = None
    company_url_direct: str | None = None

    job_type: list[JobType] | None = None
    compensation: Compensation | None = None
    date_posted: date | None = None
    emails: list[str] | None = None
    is_remote: bool | None = None

    # indeed specific
    company_addresses: str | None = None
    company_industry: str | None = None
    company_num_employees: str | None = None
    company_revenue: str | None = None
    company_description: str | None = None
    ceo_name: str | None = None
    ceo_photo_url: str | None = None
    logo_photo_url: str | None = None
    banner_photo_url: str | None = None


class JobResponse(BaseModel):
    jobs: list[JobPost] = []
