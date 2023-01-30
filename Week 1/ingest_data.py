import pandas as pd
from sqlalchemy import create_engine
import time
import os
import argparse


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # user, password, host, port, database name, table name, url of csv


    csv_name = 'output.csv'
    #parquet_name = 'output.parquet'
    os.system(f"wget {url} -O {csv_name}")
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
    df_iterator = pd.read_csv(csv_name,compression="gzip",iterator=True,chunksize=100000)



    df = next(df_iterator)

    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)




    #"""
    #**Ingesting data into PSQL database**
    #"""



    # defining the iterator that will ingest data in batches according to chunksize

    df.head(n=0).to_sql(name=table_name,con=engine,if_exists='replace')

    df.to_sql(name=table_name,con=engine,if_exists='append')

    # Batch feeding the data inside of table within database
    while True:
        t_start = time.time()
        try:
            df = next(df_iterator)
            
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            
            df.to_sql(name=table_name,con=engine,index=False,if_exists='append')
            
            t_end = time.time()
            
            print('Inserted another chunk, took {}.3f seconds'.format(t_end-t_start))
        except:
            print('All data successfully appended')
            pass
            break



if __name__=='__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')


    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port number for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of table to write data into postgres')
    parser.add_argument('--url', help='url name for postgres')


    args = parser.parse_args()

    main(args)