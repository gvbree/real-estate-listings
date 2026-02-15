import streamlit as st
import pandas as pd
import config

@st.cache_data()
def load_csv_data(
    csv_name: str,
    base_path: str = f"{config.BASE_PATH}/data"
) -> pd.DataFrame:
    
    csv_path = f"{base_path}/{csv_name}.csv"
    df = pd.read_csv(csv_path)
    print(f"Reading data from {csv_path}")

    return df