import streamlit as st
import pandas as pd
from fn.app_init_page import init_page
from fn.get_values import get_values
from fn.load_parquet_data import load_parquet_data
from fn.app_display_metadata import display_metadata
from fn.app_render_ecdf import render_ecdf
from fn.app_render_violin import render_violin
import plotly.express as px

init_page()

ad_type = st.sidebar.selectbox(
    "Ad Type", 
    ["Sale", "Rent"],
    key="sb_ad_type"
).lower()

df = load_parquet_data(ad_type)
    
with st.sidebar.expander("Comparison Settings", expanded=True):
    bdl_values = get_values(df, "bundesland", True)
    bdl = st.selectbox(
        "Bundesland", 
        bdl_values,
        key="sb_bdl"
    )
    
    filtered_df = df[df["bundesland"] == bdl] if bdl else df

    bezirk_values = get_values(filtered_df, "bezirk")
    bezirke = st.multiselect(
        "Bezirke",
        options=bezirk_values,
        default=[],
        max_selections=5
    )

    show_austria = st.checkbox("Show Austria's Average", value=True)

frames = []

if show_austria:
    df_at = df.copy()
    df_at['Group'] = "Österreich"
    frames.append(df_at)

if bdl:
    df_bdl = df[df["bundesland"] == bdl].copy()
    df_bdl['Group'] = bdl
    frames.append(df_bdl)

for b in bezirke:
    df_b = df[df['bezirk'] == b].copy()
    df_b['Group'] = b
    frames.append(df_b)

if not frames:
    st.warning("Please select a Bezirk.")
    st.stop()

compare_df = pd.concat(frames)

display_metadata(ad_type, df, compare_df, False)

view_mode = st.radio(
    "Select Visualization Type:",
    ["ECDF Plot", "Violin Plot"],
    horizontal=True,
    label_visibility="collapsed"
)

if view_mode == "Violin Plot":
    fig = render_violin(compare_df, ad_type)
else:
    fig = render_ecdf(compare_df, ad_type)
    
st.plotly_chart(fig, use_container_width=True)