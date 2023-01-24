# data-engineering-zoomcamp-2023
This Repo contains weekly learnings for data-engineering-zoomcamp 2023 course.


## Week 1
### Day 1
- [x] Introduction to the course
- [x] Introduction to the Docker
- [x] How to use Docker ENTRYPOINT for command line arguments
```bash
docker build -t test .
docker run -it test 2023-01-01
```

### Day 2
- [x] setting up the docker service for postgres
- [x] Ruuning the postgres service locally using docker
```bash
docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-p 5432:5432 \
-v /Users/mahesh.sinha/Desktop/personal/Repos/data-engineering-zoomcamp-2023/week-1-env-setup/2_docker_sql/ny_taxi_pgadmin_data:/var/lib/postgresql/data \
postgres:13.3
```
- [x] Connecting to the postgres service using pgcli
```bash
pgcli -h localhost -U root -p 5432 -d ny_taxi
```
- [x] Listing the tables in the database
```bash
\dt
```
- [x] Count the number of rows in the table
```bash
SELECT COUNT(*) FROM yellow_taxi_data;
```
- [x] Created upload_data.py script to download from web and upload the data to the postgres database.

### Day 3
- [x] Coverted the upload_data.ipynb to injest_data.py with command line arguments
```bash
python ingest_data.py \
--postgres_user="root" \
--postgres_password="root" \
--postgres_host="localhost" \
--postgres_port="5432" \
--postgres_db="ny_taxi" \
--postgres_table="yellow_taxi_trips"
```
- [x] Created a dockerfile to build the ingest-data.py script
```bash
docker build -t ingest-data:v001 .
```
- [x] Ran the injest_data.py script using docker
```bash
docker run -it ingest_data:v001 \
--postgres_user="root" \
--postgres_password="root" \
--postgres_host="localhost" \
--postgres_port="5432" \
--postgres_db="ny_taxi" \
--postgres_table="yellow_taxi_trips"
```
- [x] Created docker network to connect the postgres and injest_data containers
```bash
docker network create ny_taxi_network
```
- [x] Ran the postgres container in the network
```bash
docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-p 5432:5432 \
-v ny_taxi_postgres_data:/var/lib/postgresql/data \
--network ny_taxi_network \
--name postgres-db \
postgres:13.3
```
- [x] Ran the injest_data container in the network
```bash
docker run -it \
--network ny_taxi_network \
ingest-data:v001 \
--postgres_user="root" \
--postgres_password="root" \
--postgres_host="postgres-db" \
--postgres_port="5432" \
--postgres_db="ny_taxi" \
--postgres_table="yellow_taxi_trips"
```
- [x] Created a docker-compose.yml file to run the postgres and pgadmin containers
```bash
docker-compose up
```
- [x] Run the injest_data container:
```bash
python ingest_data.py \
--postgres_user="root" \
--postgres_password="root" \
--postgres_host="localhost" \
--postgres_port="5432" \
--postgres_db="ny_taxi" \
--postgres_table="yellow_taxi_trips"
```

### Day 4
- [x] Created taxi_zones table in the ny_taxi database from upload_data.ipynb notebook
- [x] Ran some queries on the yellow_taxi_trips and taxi_zones tables
```sql
SELECT COUNT(*) FROM yellow_taxi_trips;

SELECT COUNT(*) FROM taxi_zones;

SELECT 
tpep_pickup_datetime,
tpep_dropoff_datetime,
fare_amount,
CONCAT(zpl_id."Borough", ' / ', zpl_id."Zone") as PickupLocation,
CONCAT(zdl_id."Borough", ' / ', zdl_id."Zone") as DropoffLocation
FROM 
yellow_taxi_trips as t,
taxi_zones as zpl_id,
taxi_zones as zdl_id
WHERE 
t."PULocationID" = zpl_id."LocationID" AND
t."DOLocationID" = zdl_id."LocationID"
LIMIT 100;

SELECT 
CAST(t."tpep_pickup_datetime" as DATE) AS PickupDate,
COUNT(1) as count
FROM 
yellow_taxi_trips as t
GROUP BY (CAST(t."tpep_pickup_datetime" as DATE))
ORDER BY count DESC
LIMIT 100
```
- [x] Created GCP free tier account and created a new project.
- [x] Created a new service account and downloaded the json key file.
- [x] Edit the service account permissions to give it access to the GCP resources like BigQuery-Admin, Storage-Admin, StorageObject-Admin.
- [x] Download the gcloud sdk and installed it.
```bash
brew install --cask google-cloud-sdk
```
- [x] Setup environment variables for the service account
```bash
export GOOGLE_APPLICATION_CREDENTIALS="<path-to-service-account-json-file>"
```
- [x] Authenticated the gcloud sdk
```bash
gcloud auth application-default login
```
- [x] Download terraform and installed it.
```bash
brew install terraform
```
- [x] Created a terraform.tfvars file.
- [x] Created a main.tf file to create the GCP resources.
- [x] CReated a variables.tf file to define the variables.
- [x] Ran the terraform init command to initialize the terraform.
```bash
terraform init
```
- [x] Ran the terraform plan command to see the changes that will be made.
```bash
terraform plan
```
- [x] Ran the terraform apply command to create the resources.
```bash
terraform apply
```









