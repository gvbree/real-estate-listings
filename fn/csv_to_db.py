import config
import pandas as pd
from .postgres_connection import postgres_connect, postgres_disconnect
from .insert_sql import insert_sql

def csv_to_db(
        csv_file, 
        csv_path:str = f"{config.base_path}/data"
        ):
    df = pd.read_csv(f"{csv_path}/{csv_file}.csv")
    print(f"Reading {csv_path}/{csv_file}.csv")

    engine, conn = postgres_connect()

    insert_sql(engine, df, "dim_" + csv_file)

    postgres_disconnect(engine, conn)