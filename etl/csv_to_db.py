import config
import pandas as pd
from fn.postgres_connection import postgres_connect, postgres_disconnect
from fn.insert_sql import insert_sql

def execute(file_name:str, csv_path:str = f"{config.BASE_PATH}/data/db") -> None:
    csv_file = f"{file_name}.csv"
    df = pd.read_csv(f"{csv_path}/{csv_file}")
    print(f"Reading {csv_path}/{csv_file}")

    engine, conn = postgres_connect()

    insert_sql(engine, df, "dim_" + file_name)

    postgres_disconnect(engine, conn)