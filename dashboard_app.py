import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json

# Load stock data & analysis
stock_data = pd.read_csv("data\AMZN_cleaned.csv")
with open("data/AMZN_raw.json") as f:
    raw_json = json.load(f)
analysis = {
    "summary": "TSLA is currently in a consolidation phase...",
    "trend": "stable",
    "risk_factors": ["macro conditions", "no bullish catalysts"],
    "recommended_chart": "candlestick",
    "confidence": 85
}

# UI
st.set_page_config(page_title="Stock Insight AI", layout="wide")
st.title(f"📊 Stock Dashboard — {analysis['trend'].upper()}")

# Summary + Trend
col1, col2 = st.columns([3, 1])
col1.markdown(f"### 🧠 LLM Summary")
col1.write(analysis["summary"])
col2.metric("Confidence", f"{analysis['confidence']}%")
col2.markdown(f"**Trend:** `{analysis['trend'].capitalize()}`")

# Risk Factors
st.markdown("### ⚠️ Risk Factors")
for risk in analysis["risk_factors"]:
    st.warning(f"• {risk}")

# Chart
st.markdown("### 📈 Price Chart")
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=stock_data["timestamp"],
    open=stock_data["open"],
    high=stock_data["high"],
    low=stock_data["low"],
    close=stock_data["close"]
))
fig.update_layout(height=500, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)