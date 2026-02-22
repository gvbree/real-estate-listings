def get_values(df, col, include_blank=False):
    values = sorted(df[col].dropna().unique().tolist())

    if include_blank:
        values = [""] + values
        
    return values