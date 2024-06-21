from ingest_web_to_gcs import ingest_web_to_gcs_flow
from ingest_gcs_to_bq import ingest_gcs_to_bq_flow
from trigger_dbt import trigger_dbt_flow
from pathlib import Path
from prefect import flow
import os

@flow()
def parent_flow(kaggle_datasets: list[str] = ['rush4ratio/video-game-sales-with-ratings']) -> None:
    """
    Main function flow for prefect orchestration 
    Default set to kaggle dataset 'rush4ratio/video-game-sales-with-ratings'

    Ingestion process to GCP/BQ
    Transformation process using DBT
    """
    
    ingest_web_to_gcs_flow(kaggle_datasets) 
    dataset_dir = Path('../dataset')
    datasets = os.listdir(os.path.expanduser(dataset_dir))
    ingest_gcs_to_bq_flow(datasets)
    trigger_dbt_flow()

if __name__ == '__main__':
    kaggle_datasets = ['rush4ratio/video-game-sales-with-ratings']

    parent_flow(kaggle_datasets)