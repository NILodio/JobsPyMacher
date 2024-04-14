import logging
import os

# setting path
import pandas as pd

# importing
from jobscrapper import scrape_jobs


class JobScrapperAPI(object):
    def __init__(self, output_filepath=None):
        self.jobs_website = os.getenv("JOBS_WEBSITE")
        self.jobs_country = os.getenv("JOBS_COUNTRY")
        self.search_terms = os.getenv("SEARCH_TERMS").split(",")
        self.search_terms = [
            term.strip().lower().replace("-", " ") for term in self.search_terms
        ]
        self.logger = logging.getLogger(__name__)
        self.output_filepath = "data/raw" if not output_filepath else output_filepath

    def generate_jobs_dataset(self, num_jobs=10000, num_batch=500):
        jobs = None
        for i, search_term in enumerate(self.search_terms):
            print(
                "===== Scrapping Job ("
                + str(i + 1)
                + "/"
                + str(len(self.search_terms))
                + "):",
                search_term,
                "=====",
            )
            jobs_term = scrape_jobs(
                site_name=[self.jobs_website],
                search_term=search_term,
                country_indeed=self.jobs_country,
                hyperlinks=False,
                results_wanted=num_batch,
            )
            if jobs is not None:
                jobs = pd.concat([jobs, jobs_term], ignore_index=True)
            else:
                jobs = jobs_term.copy()

            # save CSV file checkpoint
            if not os.path.exists(f"{self.output_filepath}"):
                os.makedirs(f"{self.output_filepath}")
            jobs.to_csv(f"{self.output_filepath}/jobs_{jobs.shape[0]}.csv", index=False)
            print(f"Checkpoint saved as CSV file:'jobs_{jobs.shape[0]}.csv'")

            if len(jobs) >= num_jobs:
                print(
                    "Max amount of jobs (defined by parameter) scrpped. Ending job scrapping..."
                )
                break
