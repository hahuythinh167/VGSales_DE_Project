# Video Game Sales Data Engineering End-To-End Project

## Objective

In this project, I designed and implemented an end-to-end data pipeline to transform data from source system to an analytic dashboard. Specifically, it involved several stages:
1. Deployed the infrastructure for Google Cloud Storage (GCS) and Google BigQuery (BQ) using Terraform.
2. Extracted data from Video Game Sales dataset on Kaggle using Kaggle API in Python.
3. Load/Ingested dataset to GCS and then to BQ using Google Cloud API in Python. This process is orchestrated and automated using Prefect. 
4. Transformed, cleaned the dataset, and add additional business requirements using DBT.
5. Developed a dashboard on Looker Studio.

The primary focus of this project is to learn and understand fundamental Data Engineering core concepts with a lesser emphasis on analytics and BI development. 

## Table of Content

- [Dataset Used](#dataset-used)
- [Tools Used](#tools-used)
- [Data Pipeline Architecture](#data-pipeline-architecture)
- [Date Modeling](#data-modeling)
- [Step 1: Deploy Infrastructure](#step-1-deploy-infrastructure)
- [Step 2: Dataset Extraction](#step-2-dataset-extraction)
- [Step 3: Load](#step-3-load)
- [Step 4: Transformation](#step-4-transformation)
- [Step 5: Dashboard](#step-5-dashboard)

## Dataset Used

This project uses the Video Game Sales dataset created by RUSH KIRUBI, available on Kaggle. 

More info about the dataset can be found [here.](https://www.kaggle.com/datasets/rush4ratio/video-game-sales-with-ratings)

## Tools Used

The following tools are used in this project:
- Language: Python, SQL 
- Storage: [Google Cloud Storage](https://cloud.google.com/storage?hl=en) and [Google BigQuery](https://cloud.google.com/bigquery?hl=en)
- Transformation: [DBT](https://www.getdbt.com/)
- Orchestration: [Prefect](https://www.prefect.io/)
- Dashboard: [Looker Studio](https://lookerstudio.google.com)
- Infrastructure-as-Code: [Terraform](https://www.terraform.io/)

## Data Pipeline Architecture

<img width="897" alt="Tech-used.jpg" src="https://github.com/hahuythinh167/VGSales_DE_Project/blob/main/images/Tech-used.png">

## Step 1: Deploy Infrastructure

In this step, I initialized and deployed the infrastructure for GCS and BigQuery using Terraform. 

Here's the specific of the task that was performed:
1. Create `variables.tf` to dictate the variables used in the primary `main.tf` script. 
2. Set up `main.tf` to deploy GCS and BigQuery with variables in `variables.tf` and configuration fitting for this particular use case. 

Link to the script: [main.tf](https://github.com/hahuythinh167/VGSales_DE_Project/blob/329710b1abb14487b79323d1c916cf8e5b6a86f5/main.tf) & [variable.tf](https://github.com/hahuythinh167/VGSales_DE_Project/blob/329710b1abb14487b79323d1c916cf8e5b6a86f5/variables.tf)

```t
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.33.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

resource "google_storage_bucket" "VGSales_Bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "VGSales_dataset" {
  dataset_id = var.bq_dataset_name
}
```

```t
variable "project" {
  description = "Project Name"
  default     = "first-de-project-426107"
}

variable "credentials" {
  description = "GCP Credentials Location"
  default     = "/Users/thinhha/Documents/VGSales_DE_Project/credentials/GCP_Creds.json"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "region" {
  description = "Project Region"
  default     = "us-west1"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "VGSales_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "first-de-project-426107-terra-bucket"
}

variable "gcs_storage_class" {
  description = "GCS Bucket Storage Class"
  default     = "STANDARD"
}
```


## Step 2: Dataset Extraction

Since the dataset is from Kaggle, I utilized the Kaggle API in Python to pull the dataset from web to local machine for simplicity and automation. 

```python
def kaggle_authenticate() -> KaggleApi:

    api = KaggleApi()
    api.authenticate()

    return api

def kaggle_to_local(dataset_dir: str, kaggle_dataset: str, api) -> None:

    api.dataset_download_files(kaggle_dataset, 
                            path = Path(dataset_dir), 
                            unzip = True)
```

## Step 3: Load

After, I created the following stages:
- [Web to GCS](https://github.com/hahuythinh167/VGSales_DE_Project/blob/329710b1abb14487b79323d1c916cf8e5b6a86f5/flows/ingest_web_to_gcs.py): Using Prefect's GCP block to connect and ingest data to GCS. 
- [GCS to BQ](https://github.com/hahuythinh167/VGSales_DE_Project/blob/329710b1abb14487b79323d1c916cf8e5b6a86f5/flows/ingest_gcs_to_bq.py): Using Google Cloud API to connect and ingest data from GCS to BigQuery. 

All the stages above are orchestrated and automated using Prefect. 

![GCS Image](https://github.com/hahuythinh167/VGSales_DE_Project/blob/main/images/GCS%20image.png)

![BQ Image](https://github.com/hahuythinh167/VGSales_DE_Project/blob/main/images/BQ%20image.png)

## Step 4: Transformation

After running the Extract and Load part of the pipeline, I utilized DBT to perform the transformation part inside BigQuery. 

For this step, the transformation in DBT is divided into two stages:
- [Staging](https://github.com/hahuythinh167/VGSales_DE_Project/blob/main/dbt/models/example/staging/stg_videogame_salesdata.sql): Load raw data from BigQuery and convert columns to the appropriate data type. Minor filter and clean up for duplicate data. 
- [Core](https://github.com/hahuythinh167/VGSales_DE_Project/blob/main/dbt/models/example/core/videogame_salesdata.sql): Create surrogate key for ease of identification, apply further transformation to number and column format, and create new columns to comply with business needs. 

Staging:
```sql
{{ config(materialized='view') }}

with salesdata as (
    select *,
        row_number() over(partition by Name, Platform, Year_of_Release) as rn
    from {{ source('staging','VGSales_table')}}
)

select 
    --Identifiers
    {{ dbt_utils.generate_surrogate_key(['Name','Platform','Year_of_Release']) }} as Game_Id,
    

    --Game Info
    Name,
    Platform,
    safe_cast(Year_of_Release as integer) as Year_of_Release,
    Genre,
    Publisher,

    --Sales Info
    safe_cast(NA_Sales as numeric) as NA_Sales,
    safe_cast(EU_Sales as numeric) as EU_Sales,
    safe_cast(JP_Sales as numeric) as JP_Sales,
    safe_cast(Other_Sales as numeric) as Other_Sales,
    safe_cast(Global_Sales as numeric) as Global_Sales,

    --Ratings 
    safe_cast(Critic_Score as numeric) as Critic_Score,
    safe_cast(Critic_Count as numeric) as Critic_Count,
    safe_cast(User_Score as numeric) as User_Score,
    safe_cast(User_Count as numeric) as User_Count,
    Rating as ESRB_Rating
    
from salesdata

where rn = 1

{% if var('is_test_run', default=true) %}
    limit 100
{% endif %}
```

Core:
```sql
{{ config(materialized='table') }}

with sales_data as (
    select * from {{ ref('stg_videogame_salesdata') }}
)

select 
    --Identifier
    Game_Id,

    --Game Info
    Name,
    Platform, 
    coalesce(Year_of_Release,0) as Year_of_Release,
    Genre,
    Publisher,

    --Converting Sales Data from Million notation to normal. Convert null to 0 when applicable
    coalesce(NA_Sales*1000000,0) as NA_Sales,
    coalesce(EU_Sales*1000000,0) as EU_Sales,
    coalesce(JP_Sales*1000000,0) as JP_Sales,
    coalesce(Other_Sales*1000000,0) as Other_Sales,
    coalesce(Global_Sales*1000000,0) as Global_Sales,

    --Game Rating
    Critic_Score,
    {{ get_critic_score_category('Critic_Score') }} as Critic_Score_Category,
    User_Score,
    {{ get_user_score_category('User_Score') }} as User_Score_Category,
    ESRB_Rating,
    {{ get_ESRB_rating_full_form('ESRB_Rating') }} as ESRB_Rating_Full_Form
from 
    sales_data
```

## Step 5: Dashboard

After completing the ETL pipeline and analysis, data is loaded into a Looker Studio dashboard, and available to view [here](https://lookerstudio.google.com/u/0/reporting/cf3b0b36-8d40-4ac8-b230-adb4ff51d8ad).

![Dashboard](https://github.com/hahuythinh167/VGSales_DE_Project/blob/main/images/Dashboard.png)
***
