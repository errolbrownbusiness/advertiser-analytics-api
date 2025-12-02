from fastapi import FastAPI, Query
import pandas as pd
from pathlib import Path
from datetime import timedelta
import numpy as np
from sklearn.linear_model import LinearRegression

app = FastAPI()

# 👉 NEW ROOT ENDPOINT
@app.get("/")
def root():
    return {
        "status": "API is running! 🎉",
        "docs": "/docs",
        "message": "Welcome to the Advertiser Analytics API 🚀"
    }

# Path to your CSV file
DATA_FILE = Path(__file__).parent.parent / "data" / "advertisers_clean.csv"

def load_data():
    df = pd.read_csv(DATA_FILE)

    rename_map = {
        "order_date": "date",
        "advertiser_id": "advertiser",
        "revenue": "spend"
    }

    df.rename(columns=rename_map, inplace=True)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    for col in ["spend", "orders", "customers"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df

df = load_data()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "rows": len(df),
        "columns": df.columns.tolist()
    }

@app.get("/summary")
def summary():
    out = {}

    if "spend" in df.columns:
        out["total_revenue"] = float(df["spend"].sum())

    if "orders" in df.columns:
        out["total_orders"] = int(df["orders"].sum())

    if "customers" in df.columns:
        out["total_customers"] = int(df["customers"].sum())

    return out

@app.get("/top_advertisers")
def top_advertisers(limit: int = Query(5, ge=1, le=50)):
    if not {"advertiser", "spend"}.issubset(df.columns):
        return []

    temp = (
        df.groupby("advertiser", as_index=False)["spend"]
        .sum()
        .sort_values("spend", ascending=False)
        .head(limit)
    )

    return temp.to_dict(orient="records")

@app.get("/trend")
def trend(freq: str = Query("D", regex="^(D|W|M)$")):
    if "date" not in df.columns or "spend" not in df.columns:
        return []

    series = (
        df.set_index("date")
        .sort_index()
        .resample(freq)["spend"]
        .sum()
        .reset_index()
    )

    series["date"] = series["date"].dt.strftime("%Y-%m-%d")
    return series.to_dict(orient="records")

@app.get("/predict")
def predict(days: int = Query(7, ge=1, le=30)):
    if "date" not in df.columns or "spend" not in df.columns:
        return []

    daily = (
        df[["date", "spend"]]
        .dropna()
        .groupby("date", as_index=False)
        .sum()
        .sort_values("date")
    )

    if len(daily) < 2:
        return []

    X = daily["date"].map(pd.Timestamp.toordinal).values.reshape(-1, 1)
    y = daily["spend"].values.reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, y)

    last_date = daily["date"].max()
    future_dates = [last_date + timedelta(days=i) for i in range(1, days + 1)]
    X_future = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)
    predictions = model.predict(X_future).ravel()

    return [
        {"date": d.strftime("%Y-%m-%d"), "predicted_revenue": float(max(0, p))}
        for d, p in zip(future_dates, predictions)
    ]
