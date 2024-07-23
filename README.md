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

<img width="897" alt="Tech-used.jpg" src="https://upload.wikimedia.org/wikipedia/commons/a/a7/Blank_image.jpg">

## Step 1: Deploy Infrastructure

In this step, I initialized and deployed the infrastructure for GCS and BigQuery using Terraform. 

Here's the specific of the task that was performed:
1. Create `variables.tf` to dictate the variables used in the primary `main.tf` script. 
2. Set up `main.tf` to deploy GCS and BigQuery with variables in `variables.tf` and configuration fitting for this particular use case. 

Link to the script: (placeholder for Terraform main.tf and variables.tf scripts)

(Placeholder for Terraform script image)

## Step 2: Dataset Extraction

Since the dataset is from Kaggle, I utilized the Kaggle API in Python to pull the dataset from web to local machine for simplicity and automation. 

(placeholder for Kaggle API script. Use the ```python for this part and other script-related part)

## Step 3: Load

After, I created the following stages:
- Web to GCS: (placeholder for web to gcs script). Using Prefect's GCP block to connect and ingest data to GCS. 
- GCS to BQ: (placeholder for gcs to bq script). Using Google Cloud API to connect and ingest data from GCS to BigQuery. 

All the stages above are orchestrated and automated using Prefect. 

(placeholder for some finished task images in GCS and BQ)

## Step 4: Transformation

After running the Extract and Load part of the pipeline, I utilized DBT to perform the transformation part inside BigQuery. 

For this step, the transformation in DBT is divided into two stages:
- Staging: (placeholder link to staging sql file) Load raw data from BigQuery and convert columns to the appropriate data type. Minor filter and clean up for duplicate data. 
- Core: (placehlder link to core sql file) Create surrogate key for ease of identification, apply further transformation to number and column format, and create new columns to comply with business needs. 

(placeholder images of snapshot for data in staging and core in Bigquery)

## Step 5: Dashboard

After completing the ETL pipeline and analysis, data is loaded into a Looker Studio dashboard, and available to view [here](https://lookerstudio.google.com/u/0/reporting/cf3b0b36-8d40-4ac8-b230-adb4ff51d8ad).

(placeholder image of dashboard. format: ![]() )
***
