from fn.load_parquet_data import load_parquet_data
import streamlit as st

def display_metadata(ad_type, df_before, df_after, aggregated=True):
    load_ts_file_name = f"{ad_type}_load_ts"
    load_ts_df = load_parquet_data(load_ts_file_name)
    max_load_ts = load_ts_df['max_sys_load_ts'].iloc[0]
    max_load_ts = max_load_ts.strftime("%Y-%m-%d %H:%M")
    
    if aggregated:
        total_ads = df_before['n_ads'].sum()
        total_ads_filtered = df_after['n_ads'].sum()
    else:
        total_ads = len(df_before)
        total_ads_filtered = len(df_after)

    coverage_pct = (total_ads_filtered / total_ads) * 100 if total_ads > 0 else 0

    with st.sidebar:        
        with st.expander("Metadata", expanded=True):        
            placeholders = {
                "load_ts": st.empty(),
                "coverage": st.empty()
            }

    placeholders["load_ts"].caption(f"🔄 Data refresh: {max_load_ts}")
    placeholders["coverage"].caption(f"📊 Showing {total_ads_filtered:,.0f} ads ({coverage_pct:.1f}% of selection)")