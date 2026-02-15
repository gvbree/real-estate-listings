from fn.postgres_connection import postgres_connect, postgres_disconnect
from fn.create_supabase_driver import create_supabase_driver
from fn.build_geo_kpi_query import build_geo_kpi_query
from fn.query_to_df import query_to_df
import io

def execute():
    supabase = create_supabase_driver()
    engine, conn = postgres_connect()
    
    for ad_type in ["sale"]:
        for adm_div in ["bundesland", "bezirk", "gemeinde"]:
            query = build_geo_kpi_query(ad_type, adm_div)
            df = query_to_df(conn, query)

            buffer = io.BytesIO()
            df.to_parquet(buffer, index=False)
            buffer.seek(0)

            file_name = f"{ad_type}_kpi_{adm_div}.parquet"

            supabase.storage.from_("listings-data").upload(
                    path=file_name,
                    file=buffer.getvalue(),
                    file_options={
                        "content-type": "application/octet-stream", 
                        "upsert": "true"
                        }
                )
            print(f"Successfully uploaded {file_name} to Supabase.")

    postgres_disconnect(engine, conn)