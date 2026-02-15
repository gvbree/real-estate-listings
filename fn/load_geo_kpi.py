import streamlit as st
import pandas as pd
from fn.create_supabase_driver import create_supabase_driver
import io

@st.cache_data(ttl=3600)
def load_geo_kpi(ad_type:str, adm_div:str):
    supabase = create_supabase_driver()
    file_name = f"{ad_type}_kpi_{adm_div}.parquet"
    
    try:
        response = supabase.storage.from_("listings-data").download(file_name)
        df = pd.read_parquet(io.BytesIO(response))
        print(f"Loaded {file_name} from Supabase.")
        return df
    except Exception as e:
        st.error(f"Error loading {file_name}: {e}")
        return pd.DataFrame()