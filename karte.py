import streamlit as st
from fn.init_page import init_page
from fn.display_metadata import display_metadata
from fn.load_csv_data import load_csv_data
from fn.load_parquet_data import load_parquet_data
from fn.render_choropleth import render_choropleth
                
def get_values(df, col):
    return [""] + sorted(df[col].dropna().unique().tolist())

def sync_geo_filters(changed_key):
    if changed_key == "sb_bdlgruppe":
        st.session_state.sb_bdl = ""
        st.session_state.sb_region = ""
        st.session_state.sb_bezirk = ""
    elif changed_key == "sb_bdl":
        st.session_state.sb_region = ""
        st.session_state.sb_bezirk = ""
    elif changed_key == "sb_region":
        st.session_state.sb_bezirk = ""

def run_app():
    placeholders = init_page()
    
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                }
                footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)
    
    adm_div = st.sidebar.selectbox(
        "Administrative level", 
        ["Bundesland", "Bezirk", "Gemeinde"],
        key="sb_adm_div"
    ).lower()
    
    kpi = st.sidebar.selectbox(
        "KPI", 
        ["price_per_sqm_median", "price_median", "sqm_median", "dom_avg", "n_ads", "n_ads_per_10000p"],
        key="sb_kpi"
    )

    ad_type = st.sidebar.selectbox(
        "Ad Type", 
        ["Sale", "Rent"],
        key="sb_ad_type"
    ).lower()
    
    geo_df = load_csv_data("geo")
    
    df_bdl = geo_df.copy()
    if st.session_state.get("sb_bdlgruppe"):
        df_bdl = df_bdl[df_bdl["bundeslandgruppe"] == st.session_state["sb_bdlgruppe"]]
    
    df_region = df_bdl.copy()
    if st.session_state.get("sb_bdl"):
        df_region = df_region[df_region["bundesland"] == st.session_state["sb_bdl"]]
    
    df_bezirk = df_region.copy()
    if st.session_state.get("sb_region"):
        df_bezirk = df_bezirk[df_bezirk["region"] == st.session_state["sb_region"]]
    
    bdlgruppe_values = ["", "Ostösterreich", "Südösterreich", "Westösterreich"]
    bdl_values = get_values(df_bdl, "bundesland")
    region_values = get_values(df_region, "region")
    bezirk_values = get_values(df_bezirk, "bezirk")
    
    with st.sidebar.expander("🌍 Geographic Filters", expanded=False):
        st.selectbox("Bundeslandgruppe", 
                     bdlgruppe_values, 
                     key="sb_bdlgruppe", 
                     on_change=sync_geo_filters, args=("sb_bdlgruppe",))
        
        st.selectbox("Bundesland", 
                     bdl_values, 
                     key="sb_bdl", 
                     on_change=sync_geo_filters, args=("sb_bdl",))
        
        st.selectbox("Region", 
                     region_values, 
                     key="sb_region", 
                     on_change=sync_geo_filters, args=("sb_region",), 
                     disabled=(adm_div == "bundesland"),
                     help="Cannot filter on a location level smaller than the aggregation level.")
        
        st.selectbox("Bezirk", 
                     bezirk_values, 
                     key="sb_bezirk", 
                     on_change=sync_geo_filters, args=("sb_bezirk",), 
                     disabled=(adm_div == "bundesland"),
                     help="Cannot filter on a location level smaller than the aggregation level.")
        
    with st.sidebar.expander("🛠️ Advanced Settings", expanded=False):
        min_ads_threshold = st.number_input(
            "Min. Ads per Location",
            min_value=0,
            value=5,
            step=1,
            help="Hide locations with fewer than this many ads to avoid outlier bias."
        )
    
    filters = {}
    filters_mapping = {
        "sb_bdlgruppe": "bundeslandgruppe",
        "sb_bdl": "bundesland",
        "sb_region": "region",
        "sb_bezirk": "bezirk"
    }
    
    for sb_key, filter_key in filters_mapping.items():
        val = st.session_state.get(sb_key, "")
        if val != "":
            filters[filter_key] = val

    kpi_file_name = f"{ad_type}_kpi_{adm_div}.parquet" 
    df = load_parquet_data(kpi_file_name)
    filtered_df = df.copy()
    
    for col, val in filters.items():
        if val != "":
            filtered_df = filtered_df[filtered_df[col] == val]
            
    filtered_df = filtered_df[filtered_df['n_ads'] >= min_ads_threshold]
    
    display_metadata(placeholders, ad_type, df, filtered_df)

    if filtered_df.empty:
        st.markdown("<br><br>", unsafe_allow_html=True) 
        st.warning(f"No locations found with at least {min_ads_threshold} ads. Try lowering the threshold.")
    else:
        fig = render_choropleth(
            filtered_df,
            adm_div = adm_div, 
            kpi_name = kpi,
            ad_type = ad_type,
            filters = filters
        )
    
        st.plotly_chart(fig)
        
        df_sorted = filtered_df.sort_values(by=kpi, ascending=False)
        n_locations = len(df_sorted)
        count_to_show = 3 if n_locations >= 10 else 1
        
        top_entries = df_sorted.head(count_to_show)
        bottom_entries = df_sorted.tail(count_to_show).iloc[::-1]

        col1, col2 = st.columns(2)
        
        with col1:
            top_list = "".join([f"<div>{i}. {row[adm_div]} ({row[kpi]:,.0f})</div>" 
                                for i, (_, row) in enumerate(top_entries.iterrows(), 1)])
            
            st.markdown(f"""
                <div style="font-size: 1rem; line-height: 1.3;">
                    <strong>Highest</strong><br>{top_list}
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            bottom_list = "".join([f"<div>{i}. {row[adm_div]} ({row[kpi]:,.0f})</div>" 
                                   for i, (_, row) in enumerate(bottom_entries.iterrows(), 1)])
            
            st.markdown(f"""
                <div style="font-size: 1rem; line-height: 1.3;">
                    <strong>Lowest</strong><br>{bottom_list}
                </div>
                """, unsafe_allow_html=True)
                
run_app()