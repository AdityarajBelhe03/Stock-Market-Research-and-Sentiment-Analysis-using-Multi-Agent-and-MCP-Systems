import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import ta

def run_dashboard_agent(context: dict):
    st.set_page_config(page_title="📊 Stock Insight AI", layout="wide")

    st.title(f"📈 Analysis for {context['symbol']}")

    # 🔹 Show LLM Full Report
    st.markdown("## 🧠 DeepSeek AI Report")
    st.markdown(context["analysis_result"].get("full_report", "_No report available_"))

    # Load stock data from context
    df = context["stock_data"]
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    # ✅ Chart Selector
    chart_type = context["analysis_result"].get("recommended_chart", "candlestick").lower()
    chart_description = {
        "line": "Line Chart – Shows price trends over time.",
        "candlestick": "Candlestick Chart – Displays open, high, low, close with sentiment color.",
        "ohlc": "OHLC Bar Chart – Visualizes trading range (Open/High/Low/Close)."
    }
    st.markdown(f"### 📊 {chart_type.capitalize()} Chart")
    st.caption(chart_description.get(chart_type, ""))

    fig = go.Figure()

    if chart_type == "candlestick":
        fig.add_trace(go.Candlestick(
            x=df.index, open=df["open"], high=df["high"],
            low=df["low"], close=df["close"],
            name="Candlestick"
        ))
    elif chart_type == "ohlc":
        fig.add_trace(go.Ohlc(
            x=df.index, open=df["open"], high=df["high"],
            low=df["low"], close=df["close"],
            name="OHLC"
        ))
    else:  # Default to line
        fig.add_trace(go.Scatter(
            x=df.index, y=df["close"], mode="lines+markers",
            name="Close Price"
        ))

    fig.update_layout(template="plotly_white", height=500)
    st.plotly_chart(fig, use_container_width=True)

    # 🔍 Technical Indicators
    st.markdown("## 🔧 Technical Indicator Insights")

    # --- ATR (Volatility)
    st.subheader("ATR – Volatility")
    atr = ta.volatility.AverageTrueRange(df["high"], df["low"], df["close"]).average_true_range()
    st.line_chart(atr, use_container_width=True)

    # --- SMA & EMA (Trend)
    st.subheader("SMA & EMA – Trend Analysis")
    sma = ta.trend.SMAIndicator(df["close"], window=10).sma_indicator()
    ema = ta.trend.EMAIndicator(df["close"], window=10).ema_indicator()
    trend_df = pd.DataFrame({"SMA": sma, "EMA": ema})
    st.line_chart(trend_df, use_container_width=True)

    # --- RSI (Momentum Sentiment)
    st.subheader("RSI – Market Momentum")
    rsi = ta.momentum.RSIIndicator(df["close"]).rsi()
    st.line_chart(rsi, use_container_width=True)

    # --- OBV & Accumulation/Distribution Line
    st.subheader("OBV & A/D Line – Volume Sentiment")

# OBV as before
    obv = ta.volume.OnBalanceVolumeIndicator(df["close"], df["volume"]).on_balance_volume()

# Manual A/D Line calculation
    clv = ((df["close"] - df["low"]) - (df["high"] - df["close"])) / (df["high"] - df["low"])
    clv = clv.fillna(0)  # Avoid division by zero or NaN
    adl = (clv * df["volume"]).cumsum()

# Combine and plot
    volume_df = pd.DataFrame({"OBV": obv, "A/D Line": adl})
    st.line_chart(volume_df, use_container_width=True)


    # 🧠 Summary & Confidence
    result = context["analysis_result"]
    st.markdown("## 🔍 Summary & Market View")
    col1, col2 = st.columns(2)
    col1.markdown(f"**Trend:** `{result['trend'].capitalize()}`")
    col1.markdown(f"**Confidence:** `{result['confidence']}%`")
    col2.markdown("**Risks:**")
    for risk in result.get("risk_factors", []):
        col2.error(f"- {risk}")

    st.caption("📊 Powered by Alpha Vantage, FinBERT, DeepSeek V3, LangGraph")

# To run this:
# from dashboard_app import run_dashboard
# run_dashboard(context)