import streamlit as st
import pandas as pd
import config

@st.cache_data()
def load_geo_values():
    csv_path = f"{config.base_path}/data/geo.csv"
    df = pd.read_csv(csv_path)
    print(f"Reading Geo data from {csv_path}")

    return df