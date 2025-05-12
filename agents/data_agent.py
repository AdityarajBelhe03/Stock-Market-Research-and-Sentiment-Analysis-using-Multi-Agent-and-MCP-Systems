import requests
import pandas as pd
import os
import json
from datetime import datetime
from pathlib import Path

def run_data_agent(context: dict, config: dict) -> dict:
    print(f"🔍 [DataAgent] Fetching stock data for {context['symbol']}...")

    symbol = context["symbol"]
    interval = "60min"
    outputsize = "compact"
    api_key = config["alpha_vantage_api_key"]  # ✅ This is correct

    url = (
        f"https://www.alphavantage.co/query?"
        f"function=TIME_SERIES_INTRADAY&symbol={symbol}"
        f"&interval={interval}&outputsize={outputsize}&apikey={api_key}"
    )

    res = requests.get(url)
    data = res.json()

    key = f"Time Series ({interval})"
    if key not in data:
        print("❌ Failed to fetch stock data. Check symbol or API limits.")
        context["stock_data"] = None
        return context

    # Save raw JSON
    Path("data").mkdir(exist_ok=True)
    with open(f"data/{symbol}_raw.json", "w") as f:
        json.dump(data, f, indent=2)

    # Convert to DataFrame
    df = pd.DataFrame.from_dict(data[key], orient="index")
    df.columns = ["open", "high", "low", "close", "volume"]
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Save cleaned CSV
    df.to_csv(f"data/{symbol}_cleaned.csv")

    print("✅ Stock data fetched and saved.")
    context["stock_data"] = df  # You can also serialize if needed
    return context