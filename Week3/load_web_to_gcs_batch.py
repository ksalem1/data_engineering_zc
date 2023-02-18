import requests
import pandas as pd
from io import BytesIO
from pathlib import Path
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

@task()
def extract_from_web(url: str) -> bytes:
    r = requests.get(url)
    return r.content

@task()
def save_as_raw(content: bytes, storage_path: str) -> None:
    gcs = GcsBucket.load('zoom-gcs')
    gcs.upload_from_file_object(BytesIO(content), storage_path)


@task(log_prints=True)
def save_as_parquet(content: bytes, url: str, storage_path_parquet: str) -> pd.DataFrame:
    gcs = GcsBucket.load('zoom-gcs')
    if url.endswith('.csv'):
        df = pd.read_csv(BytesIO(content))
    if url.endswith('.csv.gz'):
        df = pd.read_csv(BytesIO(content), compression='gzip')
    df.columns = [c.lower() for c in df.columns]
    print(df.head())
    print('Rows loaded:', len(df))
    buffer = BytesIO()
    df.to_parquet(buffer, engine='auto', compression='snappy')
    buffer.seek(0)
    gcs.upload_from_file_object(buffer, storage_path_parquet)

@flow(name='Save from web to Cloud Storage')
def load_to_gcs(year: int, months: list) -> None:

    #url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_{year}-{months:02}.csv.gz'
    for month in months:
        url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_{year}-{month:02}.csv.gz'
        storage_path = f'data/fhv/fhv_tripdata_{year}-{month:02}.csv.gz'
        #storage_path_parquet = f'data/{color}/{color}_tripdata_{year}-{month:02}.parquet'

        content = extract_from_web(url)
        save_as_raw(content, storage_path)
        #save_as_parquet(content, url, storage_path_parquet)

if __name__ == '__main__':
    #color = 'yellow'
    year = 2019
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    
    load_to_gcs(year, months)