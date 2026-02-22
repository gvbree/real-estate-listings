import config
import json
import plotly.express as px
from fn.load_json_data import load_json_data

def render_choropleth(df,
                      adm_div:str,
                      kpi_name:str,
                      ad_type:str,
                      html_export:bool = False,
                      filters:dict = {},
                      simplified:str = "95"
                      ):
    with open(f"{config.BASE_PATH}/data/{adm_div}_{simplified}_geo.json") as f:
        geo = json.load(f)
    
    geo_priority = ["bezirk", "region", "bundesland", "bundeslandgruppe"]    
    filter_level = "staat"
    filter_value = "Österreich"
    
    for level in geo_priority:
        if level in filters and filters[level] != "":
            filter_level = level
            filter_value = filters[level]
            break
   
    if filters:
        subtitle_text = "Filters: " + " | ".join([f"{k} = {v}" for k, v in filters.items()])
    else:
        subtitle_text = ""

    if filter_level == "bundeslandgruppe" or filter_level == "bundesland":
        focus_level = "bundesland"
    elif filter_level == "region" or filter_level == "bezirk":
        focus_level = "bezirk"
    else:
        focus_level = "staat"
    
    if focus_level == "staat":
        center = {"lat": 47.6939, "lon": 13.3545}
        zoom = 6.8
    else:
        meta_lookup = load_json_data(f"{focus_level}_centroids")
        active_meta = [
            meta_lookup[str(n)] 
            for n in df[f"{focus_level}_iso"].unique() 
            if str(n) in meta_lookup
        ]

        if active_meta:
            all_min_lat = min(m['min_lat'] for m in active_meta)
            all_max_lat = max(m['max_lat'] for m in active_meta)
            all_min_lon = min(m['min_lon'] for m in active_meta)
            all_max_lon = max(m['max_lon'] for m in active_meta)
    
            center = {
                "lat": (all_min_lat + all_max_lat) / 2,
                "lon": (all_min_lon + all_max_lon) / 2
            }
    
            lat_spread = all_max_lat - all_min_lat
            lon_spread = all_max_lon - all_min_lon
            max_spread = max(lat_spread * 2.1, lon_spread)
            zoom = 10.5 - (max_spread * 1.0)
            zoom = max(7.2, min(zoom, 10.5))
        else:
            center = {"lat": 47.6939, "lon": 13.3545}
            zoom = 7.0
        
    print(f"\nRendering Choropleth using {adm_div}_{simplified}_geo.json, filtered on {filter_level} = {filter_value}.")
    print(f"Center: {center}, zoom: {zoom}. Calculated using the {focus_level} level.")        
    
    KPI_CONFIG = {
        "sale": {
            "price_per_sqm_median": {
                "color_range": [2500, 7500]
            },
            "price_median": {
                "color_range": [200000, 600000]
            },
            "sqm_median": {
                "color_range": [60, 140]
            },
            "default": {
                "color_range": None
            }
        },
        "rent": {
            "default": {
                "color_range": None
            }
        },
        "default": {
            "color_range": None
        }
    }
    
    kpi_cfg = KPI_CONFIG.get(ad_type, KPI_CONFIG["default"])
    kpi_cfg = kpi_cfg.get(kpi_name, kpi_cfg["default"])
    color_range = kpi_cfg["color_range"]
        
    fig = px.choropleth_mapbox(
        df,
        geojson=geo,
        locations=f"{adm_div}_iso",
        featureidkey="properties.iso",
        color=kpi_name,
        color_continuous_scale="OrRd",
        range_color=color_range,
        hover_name=adm_div,
        hover_data={
           f"{adm_div}_iso": False,
           kpi_name: ":,.0f",
           "n_ads": ":,"
        },
        mapbox_style="carto-positron",              #white-bg
        zoom=zoom,
        center=center,
        opacity=0.75
    )

    fig.update_layout(
        autosize=True,
        width=1600,
        height=700,
        margin={"r":0, "t":0, "l":0, "b":0}
    )
    
    plot_config = {
        'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'pan2d'],
        'displaylogo': True
    }
    
    if html_export:
        fig.write_html(
            "austria_choropleth.html", 
            auto_open=True, 
            config=plot_config
        )
        
    return fig