
# 📈 Stock Research & Sentiment Analysis using Multi-Agent and MCP Systems

Welcome to **Stock Insight AI** — a powerful, modular, agent-driven system that performs comprehensive stock research, sentiment analysis, technical indicator processing, and delivers personalized investment insights using LLMs and dynamic dashboards.

---

## 🚀 Project Highlights

- 🧠 **LLM-Powered Deep Analysis** (via DeepSeek V3 on OpenRouter)
- 📦 Modular **Multi-Agent** Pipeline (LangGraph-inspired)
- 🔁 **MCP Architecture**: Shared context-based communication
- 📊 Advanced **Technical Indicators** (ATR, RSI, SMA, OBV, etc.)
- 🗞️ News-based **Financial Sentiment Analysis** (via FinBERT)
- 📈 Interactive & Automated Dashboard (Plotly/Streamlit)
- 🧠 Per-indicator interpretation + full LLM narrative
- 📁 Clean structure with plug-and-play extensibility

---

## 🧱 Architecture Diagram (Node Graph)

```
           ┌──────────────┐
           │ User Input   │
           └─────┬────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ 1️⃣ DataAgent       │──▶ Retrieves stock OHLCV
        └────────┬───────────┘
                 ▼
        ┌────────────────────┐
        │ 2️⃣ NewsAgent       │──▶ Gathers latest news
        └────────┬───────────┘
                 ▼
        ┌────────────────────────┐
        │ 3️⃣ SentimentAgent      │──▶ FinBERT-based analysis
        └────────┬───────────────┘
                 ▼
        ┌────────────────────────┐
        │ 4️⃣ AnalyzerAgent       │──▶ DeepSeek LLM generates insights
        └────────┬───────────────┘
                 ▼
        ┌────────────────────────┐
        │ 5️⃣ DashboardAgent      │──▶ Generates charts & insights
        └────────────────────────┘
```

All agents read/write from a shared `context` (following the 🧠 **Model Context Protocol**).

---

## 🧠 Agent Responsibilities

| Agent           | Description |
|----------------|-------------|
| **DataAgent**     | Fetches intraday stock OHLCV from Alpha Vantage |
| **NewsAgent**     | Gets recent stock-related headlines via FinnHub |
| **SentimentAgent**| Analyzes headline sentiment using FinBERT |
| **AnalyzerAgent** | Uses DeepSeek V3 (OpenRouter) to interpret all inputs & user query |
| **DashboardAgent**| Auto-generates charts, indicators, and insights (Plotly or Streamlit) |

---

## 📊 Technical Indicators Used

| Indicator | Purpose |
|----------|---------|
| ✅ ATR (Average True Range) | Measures market volatility |
| ✅ RSI (Relative Strength Index) | Detects overbought/oversold conditions |
| ✅ SMA / EMA | Analyzes price trends |
| ✅ OBV | Tracks buying/selling pressure via volume |
| ✅ A/D Line | Assesses accumulation/distribution phase |

---

## 🧠 LLM Integration via DeepSeek V3

- Answers user queries like:  
  > *"Is this stock suitable for swing trading?"*

- Uses merged knowledge of:
  - Technical chart summaries
  - News sentiment
  - Current trends
- Returns:
  - 🧾 Full natural language report
  - 📊 Summary
  - 📉 Trend: Bullish, Bearish, or Stable
  - ⚠️ Risk factors
  - 🎯 Recommended chart

---

## 📂 File Structure

```
.
├── main.py                         # Pipeline entrypoint
├── config.yaml                    # API keys & parameters
├── agents/
│   ├── data_agent.py              # Stock data fetcher
│   ├── news_agent.py              # News API connector
│   ├── sentiment_agent.py         # FinBERT pipeline
│   ├── analyzer_agent.py          # DeepSeek LLM integration
│   └── dashboard_agent.py         # Chart & dashboard generation
├── charts/                        # Auto-saved PNG charts
├── data/                          # Stored stock & JSON results
└── dashboard_app.py               # Streamlit UI version (optional)
```

---

## 🧪 How to Run

1. ✅ Install requirements:
```bash
pip install -r requirements.txt
```

2. ✅ Run the full pipeline:
```bash
python main.py
```

3. ✅ (Optional) Launch Streamlit Dashboard:
```bash
streamlit run dashboard_app.py
```

---

## 🧠 Sample Output

```json
{
  "full_report": "TSLA is currently exhibiting strong volatility...",
  "summary": "The stock is consolidating after heavy buying pressure.",
  "trend": "stable",
  "risk_factors": ["macro uncertainty", "news sentiment"],
  "confidence": 87
}
```

---

## 🔬 Technologies Used

- 🧠 **LLM**: DeepSeek V3 via OpenRouter
- 📊 **Indicators**: `ta` (technical analysis library)
- 🎨 **Visualization**: Plotly + Streamlit
- 🗞️ **News & Sentiment**: FinnHub API + FinBERT
- 🔁 **Pipeline Design**: LangGraph-inspired agent nodes
- 🧠 **Protocol**: Model Context Protocol (MCP)

---

## 🙌 Credits

Built by **Adityaraj Sanjay Belhe**  
AI Researcher | Multi-Agent System Builder | LLM Enthusiast  
📫 [adityarajbelhe007@gamil.com](mailto:adityarajbelhe007@gamil.com)

---

## 📌 Future Enhancements

- 🗂️ LangGraph SDK integration
- 📦 PDF or CSV report export
- 📊 Per-indicator reasoning by DeepSeek
- 🌐 Streamlit Cloud Deployment

---

## 📃 License

MIT License
