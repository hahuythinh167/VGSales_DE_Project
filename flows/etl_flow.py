import pandas as pd
from pathlib import Path
from prefect import flow, task 
from kaggle.api.kaggle_api_extended import KaggleApi

def kaggle_to_local(base_dir: str, kaggle_datasets: list[str]):
    api = KaggleApi()
    api.authenticate()
    dataset_dir = f'{base_dir}/dataset'
    for dataset in kaggle_datasets:
        api.dataset_download_files(dataset, 
                                path = Path(dataset_dir), 
                                unzip = True)

if '__name__' == '__main__':
    base_dir = '/Users/thinhha/Documents/VGSales_DE_Project'
    kaggle_datasets = ['rush4ratio/video-game-sales-with-ratings']
    kaggle_to_local(base_dir, kaggle_datasets)