def insert_sql(engine, df, table):
    df.to_sql(
        table,
        engine,
        schema="ldl",
        if_exists="append",
        index=False
    )
    print(f"Inserted data into ldl.{table}")