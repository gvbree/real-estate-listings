import plotly.express as px

def get_color_map(df):
    unique_groups = df['Group'].unique()
    colors = px.colors.qualitative.Plotly
    
    color_map = {}
    dist_idx = 0
    
    sorted_groups = sorted(list(unique_groups), key=lambda x: (x != "Österreich", x))

    for g in sorted_groups:
        if g == "Österreich":
            color_map[g] = "#d73027"
        else:
            color_map[g] = colors[dist_idx % len(colors)]
            dist_idx += 1

    return color_map