import json
import config
import streamlit as st

@st.cache_data
def load_location_metadata(adm_div):
    with open(f"{config.base_path}/data/{adm_div}_centroids.json", "r", encoding='utf-8') as f:
        return json.load(f)