import pandas as pd
from fn.create_chrome_driver import create_chrome_driver
from fn.api_client import api_client
from fn.postgres_connection import postgres_connect, postgres_disconnect
from fn.insert_sql import insert_sql
from sqlalchemy import text

def execute(
        load_type:str = "preview",
        real_estate_search_types:list = ["sale_apartment", "sale_house"]
    ) -> None:

    engine, conn = postgres_connect()

    for real_estate_search_type in real_estate_search_types:
        schema = "ldl"
        table = "fact_" + real_estate_search_type

        driver = create_chrome_driver(headless = False)
        df_result = api_client(driver, real_estate_search_type, load_type)

        df = df_result.drop_duplicates().copy()
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace("/", "_", regex=False)
        )
        
        query = text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = :schema
            AND table_name = :table
            ORDER BY ordinal_position
        """)
        
        result = conn.execute(query, {"schema": schema, "table": table})
        column_names = [row[0] for row in result]    
        df.columns = df.columns.str.lower()
        
        dropped_columns = [x for x in df.columns.tolist() if x not in column_names]
        print(f"Dropped columns from DF: {dropped_columns}")
        
        df.loc[:, "sys_ad_type"] = table.split("_")[1]
        df.loc[:, "sys_property_type"] = table.split("_")[2]
        df.loc[:, "sys_load_ts"] = pd.Timestamp.now()
        sys_cols = [col for col in df.columns if col.startswith("sys")]
        print(f"Adding SYS-columns to DF: {sys_cols}")

        df = df.loc[:, df.columns.isin(column_names)]
        df = df[column_names]

        insert_sql(engine, df, table)
        
    postgres_disconnect(engine, conn)