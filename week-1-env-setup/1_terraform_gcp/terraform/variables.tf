locals {
    datalake_bucket_name = "datalake"
    bq_datawarehouse_dataset_name = "trips_data_all"
}

variable "project_id" {
    description = "The GCP project ID"
    type = string 
}

variable "region" {
    description = "The GCP region"
    type = string 
    default = "europe-west6"
}

# variable "zone" {
#     description = "The GCP zone"
#     type = string 
#     default = "europe-west6-a"
# }

variable "storage_class" {
    description = "The GCP storage class"
    type = string 
    default = "STANDARD"
}

