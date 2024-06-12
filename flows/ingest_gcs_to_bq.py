from google.cloud import bigquery
from prefect import flow, task

@task
def parameter_config():
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
    uri = "gs://first-de-project-426107-terra-bucket/dataset/Video_Games_Sales_as_at_22_Dec_2016.csv"

    return table_id, job_config, uri

@task
def load_job(client, table_id, job_config, uri):
    load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)  # Make an API request.
    print("Loaded {} rows.".format(destination_table.num_rows))

@task
def create_bq_connection():
    return bigquery.Client()

@flow
def parent_flow():
    client = create_bq_connection()

    table_id, job_config, uri = parameter_config()

    load_job(client, table_id, job_config, uri)

if __name__ == '__main__':
    parent_flow()