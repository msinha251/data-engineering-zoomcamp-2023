terraform {
    required_version = ">= 0.12.0"
    required_providers {
        google = {
            source = "hashicorp/google"
            version = "3.5.0"
        }
    }
}

provider "google" {
    #credentials = file("credentials.json") # Use this if you have a credentials file or not using environment variables
    project = var.project_id
    region = var.region
}

# Datalake bucket
resource "google_storage_bucket" "datalake-bucket" {
    name = "${local.datalake_bucket_name}_${var.project_id}"
    location = var.region
    storage_class = var.storage_class

    versioning {
        enabled = true
    }

    lifecycle_rule {
        condition {
            age = 30 # Delete objects older than 30 days
        }
        action {
            type = "Delete"
        }
    }

    force_destroy = true
}

# DataWarehouse bigquery dataset
resource "google_bigquery_dataset" "datawarehouse-dataset" {
    dataset_id = "${local.bq_datawarehouse_dataset_name}"
    location = var.region
    project = var.project_id
}


