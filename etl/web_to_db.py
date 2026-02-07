from fn.create_driver import create_driver
from fn.api_client import api_client
from fn.postgres_connection import postgres_connect, postgres_disconnect
from fn.insert_sql import insert_sql
from fn.prepare_df import prepare_df
import config

def execute(real_estate_search_type, load_type):
    real_estate_search_term = config.real_estate_types_mapping[real_estate_search_type]
    table = "fact_" + real_estate_search_type

    driver = create_driver(headless = False)
    df_result = api_client(driver, real_estate_search_term, load_type)
    
    engine, conn = postgres_connect()
    
    df = prepare_df(engine, conn, df_result, table)
    insert_sql(engine, df, table)
    
    postgres_disconnect(engine, conn)