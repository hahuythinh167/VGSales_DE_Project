from google.cloud import bigquery
from prefect import flow, task
import os
from pathlib import Path

@task(retries=3, log_prints=True)
def parameter_config(dataset: str) -> str:
    """
    Establishes dataset parameter for dataset in GCS
    """
    table_id = 'first-de-project-426107.VGSales_dataset.VGSales_table'

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("Name", "STRING"),
            bigquery.SchemaField("Platform", "STRING"),
            bigquery.SchemaField("Year_of_Release", "STRING"),
            bigquery.SchemaField("Genre", "STRING"),
            bigquery.SchemaField("Publisher", "STRING"),
            bigquery.SchemaField("NA_Sales", "STRING"),
            bigquery.SchemaField("EU_Sales", "STRING"),
            bigquery.SchemaField("JP_Sales", "STRING"),
            bigquery.SchemaField("Other_Sales", "STRING"),
            bigquery.SchemaField("Global_Sales", "STRING"),
            bigquery.SchemaField("Critic_Score", "STRING"),
            bigquery.SchemaField("Critic_Count", "STRING"),
            bigquery.SchemaField("User_Score", "STRING"),
            bigquery.SchemaField("User_Count", "STRING"),
            bigquery.SchemaField("Developer", "STRING"),
            bigquery.SchemaField("Rating", "STRING"),
        ],
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
    )
    uri = f'gs://first-de-project-426107-terra-bucket/dataset/{dataset}'

    return table_id, job_config, uri

@task(retries=3, log_prints=True)
def load_job(client, table_id: str, job_config, uri: str):
    """
    Loads dataset from GCS to BigQuery Data Warehouse using Google Cloud API
    """
    load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)  # Make an API request.
    print("Loaded {} rows.".format(destination_table.num_rows))

@task()
def create_bq_connection() -> bigquery.Client:
    """
    Connects to BigQuery Client using Google Cloud API
    """

    return bigquery.Client()

@flow()
def ingest_gcs_to_bq_flow(datasets: list[str]):
    """
    Ingest files from GCS to BigQuery using Google Cloud API

    Creates connection to BigQuery
    Establishes parameter list for datasets in GCS 
    Loads to BigQuery Data Warehouse using Google Cloud API
    """
    client = create_bq_connection()

    for dataset in datasets:
        table_id, job_config, uri = parameter_config(dataset)

        load_job(client, table_id, job_config, uri)

if __name__ == '__main__':
    dataset_dir = Path('../dataset')
    datasets = os.listdir(os.path.expanduser(dataset_dir))
    
    ingest_gcs_to_bq_flow(datasets)