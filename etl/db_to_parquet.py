from fn.postgres_connection import postgres_connect, postgres_disconnect
from fn.create_supabase_driver import create_supabase_driver
from fn.query_to_df import query_to_df
from fn.df_to_supabase import df_to_supabase

def execute(ad_types: list = ["sale", "rent"]) -> None:
    supabase = create_supabase_driver()
    engine, conn = postgres_connect()
    
    for ad_type in ad_types:
        # data
        query = f"""
        SELECT *
        FROM ldl.{ad_type}
        """
        df = query_to_df(conn, query)
        df_to_supabase(supabase, df, file_name = ad_type)

        # load_ts
        query = f"""
        SELECT MIN(sys_load_ts) AS max_sys_load_ts
        FROM ldl.{ad_type}
        """
        df = query_to_df(conn, query)
        df_to_supabase(supabase, df, file_name = f"{ad_type}_load_ts")

    postgres_disconnect(engine, conn)