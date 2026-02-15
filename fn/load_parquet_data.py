import streamlit as st
import pandas as pd
from fn.create_supabase_driver import create_supabase_driver
import io

@st.cache_data(ttl=3600)
def load_parquet_data(file_name:str) -> pd.DataFrame:
    supabase = create_supabase_driver()
    
    try:
        response = supabase.storage.from_("listings-data").download(file_name)
        df = pd.read_parquet(io.BytesIO(response))
        print(f"Loaded {file_name} from Supabase.")
        return df
    except Exception as e:
        st.error(f"Error loading {file_name}: {e}")
        return pd.DataFrame()