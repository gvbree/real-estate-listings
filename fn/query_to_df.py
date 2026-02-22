from sqlalchemy import text
import pandas as pd

def query_to_df(conn, query:str):    
    print(f"Executing query:{query}")
    df = pd.read_sql(text(query), conn) 
        
    return df