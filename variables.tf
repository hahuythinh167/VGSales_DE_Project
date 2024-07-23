variable "project" {
  description = "Project Name"
  default     = "first-de-project-426107"
}

variable "credentials" {
  description = "GCP Credentials Location"
<<<<<<< HEAD
  default     = "/Users/thinhha/Documents/VGSales_DE_Project/credentials/GCP_Creds.json"
=======
  default     = "/Users/thinhha/Documents/DE First Project/credentials/GCP_Creds.json"
>>>>>>> 0a45c1d (Add configuration for BigQuery in Terraform file)
}

variable "location" {
  description = "Project Location"
<<<<<<< HEAD
  default     = "US"
=======
  default     = "ASIA"
>>>>>>> 0a45c1d (Add configuration for BigQuery in Terraform file)
}

variable "region" {
  description = "Project Region"
<<<<<<< HEAD
  default     = "us-west1"
=======
  default     = "asia-southeast1"
>>>>>>> 0a45c1d (Add configuration for BigQuery in Terraform file)
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