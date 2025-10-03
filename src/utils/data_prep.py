import pandas as pd

def parse_dt(df, cols=["timestamp"]):
    for col in cols:
        df[col] = pd.to_datetime(
            df[col],
            errors="coerce",   # tránh crash khi dữ liệu không hợp lệ
            unit="s" if df[col].astype(str).str.len().max() <= 10 else "ms"
        )
    return df

def handle_dtypes(df):
    return df.assign(rating=lambda df: df["rating"].astype(float))
