from sqlalchemy import text
import pandas as pd

def prepare_df(engine, conn, df, table):
    schema = "ldl"
    
    df.columns = (
        df.columns
          .str.strip()
          .str.lower()
          .str.replace("/", "_", regex=False)
    )
    
    query = text("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = :schema
          AND table_name = :table
        ORDER BY ordinal_position
    """)
    
    result = conn.execute(query, {"schema": schema, "table": table})
    column_names = [row[0] for row in result]    
    df.columns = df.columns.str.lower()
    
    dropped_columns = [x for x in df.columns.tolist() if x not in column_names]
    print(f"Dropped columns from DF: {dropped_columns}")
    
    df["sys_ad_type"] = table.split("_")[1]
    df["sys_property_type"] = table.split("_")[2]
    df["sys_load_ts"] = pd.Timestamp.now()
    sys_cols = [col for col in df.columns if col.startswith("sys")]
    print(f"Adding SYS-columns to DF: {sys_cols}")

    df = df.loc[:, df.columns.isin(column_names)]
    df = df[column_names]
    
    return df