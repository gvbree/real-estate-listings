import plotly.express as px
from fn.app_get_color_map import get_color_map

def render_ecdf(df, ad_type):
    color_map = get_color_map(df)
    range = [0, 1000000] if ad_type == "sale" else [0, 3000]

    fig = px.ecdf(
        df, 
        x="price", 
        color="Group",
        range_x=range,
        color_discrete_map=color_map
    )
    fig.update_layout(
        xaxis_title="Price in €",
        yaxis_title="Share of Properties (Cumulative)",
        margin=dict(t=10, b=10, l=10, r=10),
        legend_title=None,
        height=700
    )

    return fig