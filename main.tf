terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "5.33.0"
    }
  }
}

provider "google" {
  project     = "first-de-project-426107"
  region      = "us-central1"

}

resource "google_storage_bucket" "DE-Project-VGSales" {
  name          = "first-de-project-426107-terra-bucket"
  location      = "US"
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