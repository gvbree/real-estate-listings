import streamlit as st
import pandas as pd
from fn.create_supabase_driver import create_supabase_driver
import io

@st.cache_data(ttl=3600)
def load_parquet_data(file_name:str) -> pd.DataFrame:
    supabase = create_supabase_driver()
    parquet_file = f"{file_name}.parquet"
    
    try:
        response = supabase.storage.from_("listings-data").download(parquet_file)
        df = pd.read_parquet(io.BytesIO(response))
        print(f"Loaded {parquet_file} from Supabase.")
        return df
    except Exception as e:
        st.error(f"Error loading {parquet_file}: {e}")
        return pd.DataFrame()