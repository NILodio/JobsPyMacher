from __future__ import annotations

from ..jobs import BaseModel, Country, DescriptionFormat, Enum, JobResponse, JobType


class Site(Enum):
    INDEED = "indeed"
    GLASSDOOR = "glassdoor"


class ScraperInput(BaseModel):
    site_type: list[Site]
    search_term: str | None = None
    location: str | None = None
    country: Country | None = Country.CANADA
    distance: int | None = None
    is_remote: bool = False
    job_type: JobType | None = None
    easy_apply: bool | None = None
    offset: int = 0
    # linkedin_fetch_description: bool = False
    # linkedin_company_ids: list[int] | None = None
    description_format: DescriptionFormat | None = DescriptionFormat.MARKDOWN

    results_wanted: int = 15
    hours_old: int | None = None


class Scraper:
    def __init__(self, site: Site, proxy: list[str] | None = None):
        self.site = site
        self.proxy = (lambda p: {"http": p, "https": p} if p else None)(proxy)

    def scrape(self, scraper_input: ScraperInput) -> JobResponse: ...
