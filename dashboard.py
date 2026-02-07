import streamlit as st
from fn.load_geo_values import load_geo_values
from fn.load_geo_kpi import load_geo_kpi
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
    st.set_page_config(
        page_title="Real Estate Austria",
        layout="wide"
    )
    
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                }
                footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)
        
    coverage_placeholder = st.sidebar.empty()
    st.sidebar.header("Configuration")

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
    
    geo_df = load_geo_values()
    
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
    
    with st.sidebar.expander("🌍 Geographic Filters", expanded=True):
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
        
    with st.sidebar.expander("🚫 Exclude Bezirke", expanded=False):
        to_exclude = st.multiselect(
            "Select Bezirke to hide:",
            options=[v for v in bezirk_values if v != "" and v != "Wien"],
            help="Hidden Bezirke will not be used for color scaling or shown on the map."
        )
        
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
          
    df = load_geo_kpi("sale", adm_div)
    filtered_df = df.copy()
        
    if to_exclude:
        filtered_df = filtered_df[~filtered_df[adm_div].isin(to_exclude)]
    
    for col, val in filters.items():
        if val != "":
            filtered_df = filtered_df[filtered_df[col] == val]
            
    filtered_df = filtered_df[filtered_df['n_ads'] >= min_ads_threshold]
    
    total_ads = df['n_ads'].sum()
    total_ads_filtered = filtered_df['n_ads'].sum()
    coverage_pct = (total_ads_filtered / total_ads) * 100 if total_ads > 0 else 0
    coverage_placeholder.caption(f"📊 Showing {total_ads_filtered:,.0f} ads ({coverage_pct:.1f}% of selection)")
    
    if filtered_df.empty:
        st.markdown("<br><br>", unsafe_allow_html=True) 
        st.warning(f"No locations found with at least {min_ads_threshold} ads. Try lowering the threshold.")
    else:
        fig = render_choropleth(
            filtered_df,
            adm_div = adm_div, 
            kpi_name = kpi,
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