import streamlit as st
import json
import config

@st.cache_data()
def load_json_data(
    json_name: str, 
    base_path: str = f"{config.BASE_PATH}/data"
) -> dict:
    
    json_path = f"{base_path}/{json_name}.json"
    with open(json_path, "r", encoding='utf-8') as f:
        data = json.load(f)
        f.close()

    print(f"Reading data from {json_path}")
    return data