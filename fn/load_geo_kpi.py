import streamlit as st
import pandas as pd
import config

@st.cache_data
def load_geo_kpi(ad_type:str, adm_div:str):
    path = f"{config.base_path}/data/{ad_type}_kpi_{adm_div}.parquet"
    
    print(f"Loading Parquet-data from {path}")
    return pd.read_parquet(path)