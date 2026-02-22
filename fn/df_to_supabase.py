import io
from fn.create_supabase_driver import create_supabase_driver

def df_to_supabase(supabase, df, file_name):
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    parquet_file = f"{file_name}.parquet"

    supabase.storage.from_("listings-data").upload(
            path=parquet_file,
            file=buffer.getvalue(),
            file_options={
                "content-type": "application/octet-stream", 
                "upsert": "true"
                }
        )
    print(f"Successfully uploaded {parquet_file} to Supabase.\n")