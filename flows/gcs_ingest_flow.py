from pathlib import Path
from prefect import flow, task 
from kaggle.api.kaggle_api_extended import KaggleApi
from prefect_gcp.cloud_storage import GcsBucket
import os

@task
def local_path(filename: str, dataset_dir: str = '/Users/thinhha/Documents/VGSales_DE_Project/dataset') -> Path:
    """
    Create path for local machine
    """
    return Path(f'{dataset_dir}/{filename}')

@task
def remote_path(filename: str) -> Path:
    """
    Create path for remote instance e.g. GCS
    """
    return Path(f'dataset/{filename}')

@task
def kaggle_to_local(dataset_dir: str, kaggle_dataset: str, api) -> None:
    """
    Connects to kaggle api, fetches kaggle dataset, and writes dataset to designated folder
    """

    api.dataset_download_files(kaggle_dataset, 
                            path = Path(dataset_dir), 
                            unzip = True)

@task
def kaggle_authenticate():
    api = KaggleApi()
    api.authenticate()

    return api

@task
def write_gcs(dataset: str) -> None:
    """
    Write dataset files to GCS Bucket through Prefect Block
    """
    path = Path(f'dataset/{dataset}')
    local_path = Path(f'../{path}')
    remote_path = path

    gcp_cloud_storage_bucket_block = GcsBucket.load('vgsales-gcsbucket-block')
    gcp_cloud_storage_bucket_block.upload_from_path(from_path=local_path, to_path=remote_path)

@flow()
def parent_flow(dataset_dir: Path, kaggle_datasets: list[str]) -> None:
    api = kaggle_authenticate()
    for kaggle_dataset in kaggle_datasets:
        kaggle_to_local(dataset_dir, kaggle_dataset, api)
    datasets = os.listdir(os.path.expanduser(dataset_dir))
    
    for dataset in datasets:
        write_gcs(dataset)

if __name__  == '__main__':
    base_dir = Path('/Users/thinhha/Documents/VGSales_DE_Project')
    dataset_dir = Path(f'{base_dir}/dataset')
    kaggle_datasets = ['rush4ratio/video-game-sales-with-ratings']

    parent_flow(dataset_dir, kaggle_datasets)