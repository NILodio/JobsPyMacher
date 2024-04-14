# -*- coding: utf-8 -*-
import logging
import os
from pathlib import Path

import click
from dotenv import find_dotenv, load_dotenv
from job_scrapper import JobScrapperAPI

from resumes_kaggle import get_kaggle_data


@click.command()
@click.argument("output_filepath", type=click.Path())
@click.option("--job_posts", default=True, help="Download job posts data.")
@click.option("--num_jobs", default=10000, help="Number of jobs to fetch.")
@click.option("--num_batch", default=500, help="Number of jobs per search term.")
@click.option("--kaggle_data", default=True, help="Download Kaggle data.")
def main(
    output_filepath, num_jobs=10000, num_batch=500, kaggle_data=False, job_posts=False
):
    """Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../processed).
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Starting data processing...")

    if job_posts:
        logger.info(
            f"Creating JobScrapperAPI to get job posts dataset with <={num_jobs} rows"
        )
        data = JobScrapperAPI(output_filepath=output_filepath)
        data.generate_jobs_dataset(num_jobs=num_jobs, num_batch=num_batch)
    if kaggle_data:
        logger.info("Downloading Kaggle data...")
        get_kaggle_data(
            dataset_name=os.getenv("KAGGLE_DATASET"), download_path=output_filepath
        )


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
