import streamlit as st
import pandas as pd
from fn.load_parquet_data import load_parquet_data
from fn.load_csv_data import load_csv_data

@st.cache_data
def get_aggregated_data(ad_type, adm_div):
    id_col = f"{adm_div}_iso"

    df = load_parquet_data(ad_type)

    df['price_per_sqm'] = df['price'] / df['estate_size_living_area']
    df['days_on_market'] = (df['sys_load_ts'] - df['published_string']).dt.days
    
    agg_dict = {
        'price_per_sqm_median': ('price_per_sqm', 'median'),
        'price_median': ('price', 'median'),
        'sqm_median': ('estate_size_living_area', 'median'),
        'days_on_market_avg': ('days_on_market', 'mean'),
        'n_ads': ('adid', 'count'),
    }
    
    potential_location_cols = [
        "bundeslandgruppe", "bundeslandgruppe_iso", "bundesland", "bundesland_iso", 
        "region", "region_iso", "bezirk", "bezirk_iso", "gemeinde", "gemeinde_iso"
    ]
    
    for col in potential_location_cols:
        if col in df.columns and col != id_col:
            if adm_div == "bundesland" and ("bezirk" in col or "gemeinde" in col): continue
            if adm_div == "bezirk" and "gemeinde" in col: continue

            agg_dict[col] = (col, "first")
    
    agg_df = df.groupby(id_col).agg(**agg_dict).reset_index()

    pop_df = load_csv_data("population")
    pop_df = pop_df[pop_df['level'] == adm_div].copy()
    
    agg_df[f"{adm_div}_iso"] = agg_df[f"{adm_div}_iso"].astype(str)
    pop_df['iso'] = pop_df['iso'].astype(str)

    final_df = pd.merge(
        pop_df, 
        agg_df, 
        left_on='iso', 
        right_on=f"{adm_div}_iso", 
        how='left'
    )

    final_df['n_ads_per_10000p'] = (final_df['n_ads'] * 10000) / final_df['population']
    
    return final_df