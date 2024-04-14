import logging
import os
import subprocess
import zipfile

logger = logging.getLogger(__file__)


class KaggleDatasetDownloader:
    def __init__(self, dataset_name, download_path="."):
        self.dataset_name = dataset_name
        self.download_path = download_path

    def download_dataset(self):
        if not os.path.exists(f"{self.download_path}"):
            os.makedirs(f"{self.download_path}")
        command = (
            f"kaggle datasets download -d {self.dataset_name} -p {self.download_path}"
        )

        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error downloading dataset '{self.dataset_name}': {e}")

    def extract_zip(self):
        zip_file_path = os.path.join(
            self.download_path, f'{self.dataset_name.split("/")[1]}.zip'
        )
        extract_path = os.path.join(self.download_path, "extracted")

        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)


def get_kaggle_data(
    dataset_name: str = "snehaanbhawal/resume-dataset",
    download_path: str = "./data/raw",
):
    logger.info(f"Downloading Kaggle dataset: {dataset_name} to {download_path}")
    downloader = KaggleDatasetDownloader(dataset_name, download_path)
    downloader.download_dataset()
    downloader.extract_zip()
