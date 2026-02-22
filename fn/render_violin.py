import plotly.express as px
from fn.get_color_map import get_color_map

def render_violin(df, ad_type):
    color_map = get_color_map(df)
    range = [0, 1000000] if ad_type == "sale" else [0, 3000]

    fig = px.violin(
        df, 
        x="Group", 
        y="price", 
        color="Group",
        range_y=range,
        box=True,
        points=None,
        color_discrete_map=color_map
    )

    fig.update_layout(
        yaxis_title="Price in €",
        xaxis_title=None,
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=False,
        height=700
    )

    return fig