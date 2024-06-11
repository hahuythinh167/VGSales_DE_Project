variable "project" {
  description = "Project Name"
  default     = "first-de-project-426107"
}

variable "credentials" {
  description = "GCP Credentials Location"
  default     = "/Users/thinhha/Documents/DE First Project/credentials/GCP_Creds.json"
}

variable "location" {
  description = "Project Location"
  default     = "ASIA"
}

variable "region" {
  description = "Project Region"
  default     = "asia-southeast1"
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