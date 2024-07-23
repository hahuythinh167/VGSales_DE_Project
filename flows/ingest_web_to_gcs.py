from pathlib import Path
from prefect import flow, task 
from kaggle.api.kaggle_api_extended import KaggleApi
from prefect_gcp.cloud_storage import GcsBucket
import os

@task(log_prints=True)
def kaggle_to_local(dataset_dir: str, kaggle_dataset: str, api) -> None:
    """
    Connects to Kaggle API, fetches kaggle dataset, and writes dataset to predetermined directory
    """

    api.dataset_download_files(kaggle_dataset, 
                            path = Path(dataset_dir), 
                            unzip = True)

@task
def kaggle_authenticate() -> KaggleApi:
    """
    Authenticates Kaggle API
    """
    api = KaggleApi()
    api.authenticate()

    return api

@task(retries=3, log_prints=True)
def write_gcs(dataset: str) -> None:
    """
    Write dataset files to GCS Bucket using Prefect Block
    """
    path = Path(f'dataset/{dataset}')
    local_path = Path(f'../{path}')
    remote_path = path

    gcp_cloud_storage_bucket_block = GcsBucket.load('vgsales-gcsbucket-block')
    gcp_cloud_storage_bucket_block.upload_from_path(from_path=local_path, to_path=remote_path)

@flow()
def ingest_web_to_gcs_flow(kaggle_datasets: list[str] = ['rush4ratio/video-game-sales-with-ratings']) -> None:
    """
    Main flow for ingestion process from web to GCS
    
    Using Kaggle API to pull datasets to local machine
    Write dataset files to GCS using connected blocks in Prefect 
    """
    dataset_dir = Path('../dataset')

    api = kaggle_authenticate()
    for kaggle_dataset in kaggle_datasets:
        kaggle_to_local(dataset_dir, kaggle_dataset, api)
    datasets = os.listdir(os.path.expanduser(dataset_dir))
    
    for dataset in datasets:
        write_gcs(dataset)

if __name__  == '__main__':
    kaggle_datasets = ['rush4ratio/video-game-sales-with-ratings']

    ingest_web_to_gcs_flow(kaggle_datasets) 