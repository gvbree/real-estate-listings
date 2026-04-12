# real-estate-listings
The real estate market is interesting for many macro-economic purposes. This showcase project extracts Austrian real estate listing data from the web. The data is then cleaned, processed, enriched with other data, and eventually visualized in a simple interactive Streamlit dashboard. 

## Purpose & Disclaimer
This private project was built strictly for **learning and showcase purposes** and has no commercial intent. It serves as a personal deep-dive into the architecture design, geographical data visualization, and deployment learning purposes.

## Architecture
Web -> Postgres (local) -> Supabase bucket (cloud) -> Streamlit dashboard

## Dashboard
All graphs are made with plotly. For the choropleth, the GeoJSONs of https://github.com/ginseng666/GeoJSON-TopoJSON-Austria/tree/master are used. Population and geographical data comes from Statistik Austria.

The dashboard consists of two pages: *Karte* (map) and *Bezirksvergleicher* (district comparison tool). 
- The *Karte* serves to provide a nice visual overview of several KPIs, such as median price per square meter, median pice, median square meters, average days-on-market, number of ads, and number of ads per 10.000 inhabitants. These provide insights in regional differences in prices, real estate size, and supply (per capita). Three aggregation levels are available: Bundesland (province), Bezirk (district) and Gemeinde (municipality). Extended geographical filter possibilities are available. By default, locations with less than 5 listings are filtered out, to prevent misleading conclusions caused by outliers.
- The *Bezirksvergleicher* is a tool to select and compare prices among districts and Austria's average. It offers a ECDF (Empirical Cumulative Distribution Function) plot and a violin plot, which both enable clear price comparison at first sight.

## Deployment
For learning purposes, two deployment methods were successfully implemented:
- using Kubernetes & Rancher
- using Streamlit Cloud

## Access
This dashboard is part of a private project and is not publicly accessible. The listings dataset used by the dashboard is also not distributed.

For the private access, uptime of the Supabase-backend data is maintained through a GitHub Action. Status:
[![Supabase Keep Alive](https://github.com/gvbree/real-estate-listings/actions/workflows/supabase_keep_alive.yml/badge.svg)](https://github.com/gvbree/real-estate-listings/actions)

## Demo
![Choropleth - Bezirk level - Austria](https://phcapxmqcsxtclmwbflc.supabase.co/storage/v1/object/public/dashboard-demo/choropleth_1.png)
![Choropleth - Gemeinde level - Klagenfurt-Villach](https://phcapxmqcsxtclmwbflc.supabase.co/storage/v1/object/public/dashboard-demo/choropleth_2.png)
![ECDF](https://phcapxmqcsxtclmwbflc.supabase.co/storage/v1/object/public/dashboard-demo/ecdf_1.png)
![Violin](https://phcapxmqcsxtclmwbflc.supabase.co/storage/v1/object/public/dashboard-demo/violin_1.png)
