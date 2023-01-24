import os
import argparse
from sqlalchemy import create_engine
import pandas as pd
from time import time

def main(params):
    data_path = "output.csv.gz"
   
    # create engine
    engine = create_engine(f'postgresql://{params.postgres_user}:{params.postgres_password}@{params.postgres_host}:{params.postgres_port}/{params.postgres_db}')
    engine.connect()

    # read data
    chunksize = 1000000
    df_iter = pd.read_csv(data_path, chunksize=chunksize, iterator=True)
    df = next(df_iter)

    # conver tpep_pickup_datetime and tpep_dropoff_datetime to datetime
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

    # create table
    df.head(0).to_sql('yellow_taxi_data', con=engine, if_exists='replace')

    # insert data into table
    while True:
        try:
            start = time()
            df = next(df_iter)
            df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
            df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
            df.to_sql(params.postgres_table, con=engine, if_exists='append', index=False)
            end = time()
            print(f'Another chunk inserted, time taken: {end-start}')
        except StopIteration:
            print("Data ingestion completed")
            break

if __name__ == "__main__":
    # Download the data from the URL
    URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz"
    os.system(f"wget {URL} -O output.csv.gz")

    parser = argparse.ArgumentParser(description="Download nyc taxi data and ingest into postgres")
    parser.add_argument("--postgres_user", type=str, default="root")
    parser.add_argument("--postgres_password", type=str, default="root")
    parser.add_argument("--postgres_host", type=str, default="localhost")
    parser.add_argument("--postgres_port", type=str, default="5432")
    parser.add_argument("--postgres_db", type=str, default="ny_taxi")
    parser.add_argument("--postgres_table", type=str, default="yellow_taxi_trips")
    args = parser.parse_args()

    main(args)
    


