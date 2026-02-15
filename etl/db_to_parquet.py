from fn.postgres_connection import postgres_connect, postgres_disconnect
from fn.create_supabase_driver import create_supabase_driver
from fn.build_geo_kpi_query import build_geo_kpi_query
from fn.query_to_df import query_to_df
from fn.df_to_supabase import df_to_supabase

def execute():
    supabase = create_supabase_driver()
    engine, conn = postgres_connect()
    
    for ad_type in ["sale"]:
        for adm_div in ["bundesland", "bezirk", "gemeinde"]:
            file_name = f"{ad_type}_kpi_{adm_div}.parquet"

            query = build_geo_kpi_query(ad_type, adm_div)
            df = query_to_df(conn, query)
            df_to_supabase(supabase, df, file_name)

        file_name = f"{ad_type}_max_sys_load_ts.parquet"

        query = f"""
        SELECT MIN(sys_load_ts) AS max_sys_load_ts
        FROM ldl.{ad_type}
        """
        df = query_to_df(conn, query)
        df_to_supabase(supabase, df, file_name)

    postgres_disconnect(engine, conn)