from fn.postgres_connection import postgres_connect, postgres_disconnect
from fn.build_geo_kpi_query import build_geo_kpi_query
from fn.query_to_df import query_to_df
import config

def execute():
    engine, conn = postgres_connect()
    
    for ad_type in ["sale"]:
        for adm_div in ["bundesland", "bezirk", "gemeinde"]:
            query = build_geo_kpi_query(ad_type, adm_div)
            df = query_to_df(conn, query)
            df.to_parquet(f"{config.base_path}/data/{ad_type}_kpi_{adm_div}.parquet")
    
    postgres_disconnect(engine, conn)