from fn.create_chrome_driver import create_chrome_driver
from fn.api_client import api_client
from fn.postgres_connection import postgres_connect, postgres_disconnect
from fn.insert_sql import insert_sql
from fn.prepare_df import prepare_df

def execute(
        load_type:str = "preview",
        real_estate_search_types:list = ["sale_apartment", "sale_house"]
        ) -> None:

    engine, conn = postgres_connect()

    for real_estate_search_type in real_estate_search_types:
        table = "fact_" + real_estate_search_type

        driver = create_chrome_driver(headless = False)
        df_result = api_client(driver, real_estate_search_type, load_type)
        df = prepare_df(engine, conn, df_result, table)
        insert_sql(engine, df, table)
        
    postgres_disconnect(engine, conn)