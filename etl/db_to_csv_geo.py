from fn.query_to_df import query_to_df
import config

def execute() -> None:
    query = """
    select bundeslandgruppe, bundesland, region, bezirk
    from ldl.dim_bezirk_region br
    join ldl.dim_bundesland_gruppe bg
    on left(br.bezirk_iso::text, 1) = bg.bundesland_iso::text
    order by bundeslandgruppe_iso, bundesland_iso, region_iso, bezirk_iso
    """
    
    df = query_to_df(query)
    csv_path = f"{config.BASE_PATH}/data/geo.csv"
    
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"Created {csv_path} successfully!")