import os
import json
import requests
import re

def extract_json_block(raw_output):
    """
    Try to clean LLM output by extracting valid JSON block.
    """
    # Try to match a ```json ... ``` block
    md_match = re.search(r"```(?:json)?(.*?)```", raw_output, re.DOTALL)
    if md_match:
        return md_match.group(1).strip()

    # Try to extract from raw string starting with '{' and ending with '}'
    fallback_match = re.search(r"\{.*\}", raw_output, re.DOTALL)
    if fallback_match:
        return fallback_match.group(0).strip()

    return raw_output.strip()

def format_data_for_prompt(context):
    stock_data_df = context.get("stock_data")
    sentiment = context.get("sentiment_summary", {}).get("overall", "NEUTRAL")
    headlines = context.get("headlines", [])
    user_query = context.get("user_query", "")
    symbol = context.get("symbol")

    # Extract recent stock rows
    if stock_data_df is not None:
        recent_data = stock_data_df.tail(5).to_dict(orient="records")
    else:
        recent_data = "No stock data available."

    return {
        "symbol": symbol,
        "recent_stock_data": recent_data,
        "news_sentiment": sentiment,
        "headlines": headlines,
        "user_query": user_query
    }

def build_prompt(merged):
    return [
        {
            "role": "system",
            "content": (
                "You are a professional financial analyst AI. "
                "You must respond in raw, valid JSON format only. "
                "No markdown. No code blocks. No explanations."
            )
        },
        {
            "role": "user",
            "content": f"""
Analyze the following inputs and generate an intelligent, natural-language report:

- Stock Symbol: {merged['symbol']}
- Latest OHLC Data: {json.dumps(merged['recent_stock_data'], indent=2)}
- Headlines: {json.dumps(merged['headlines'], indent=2)}
- News Sentiment: {merged['news_sentiment']}
- User Query: {merged['user_query']}

Respond in JSON with the following fields:
- 'full_report': 1–2 paragraphs directly answering the user query, combining technical and sentiment analysis
- 'summary': concise technical summary (1 para)
- 'trend': bullish, bearish, or stable
- 'risk_factors': list of 1–3 relevant risks
- 'recommended_chart': one of 'line', 'candlestick', or 'ohlc'
- 'confidence': a number from 0 to 100
"""
        }
    ]

def query_deepseek(messages, api_key, model):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://yourdomain.com",
        "Content-Type": "application/json"
    }

    payload = {
    "model": model,
    "messages": messages,
    "temperature": 0.4,      # more factual
    "top_p": 0.95,
    "max_tokens": 1200       # increased from default
    }


    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

def run_analyzer_agent(context: dict, config: dict) -> dict:
    print("📊 [AnalyzerAgent] Running DeepSeek LLM for market insight...")

    merged = format_data_for_prompt(context)
    messages = build_prompt(merged)

    result = query_deepseek(
        messages=messages,
        api_key=config["openrouter_api_key"],
        model=config["deepseek_model"]
    )

    print("🔎 Raw LLM Output:\n", result)

    # NEW: Extract JSON safely even from mixed content
    clean_json_str = extract_json_block(result)

    try:
        result_json = json.loads(clean_json_str)
        print("✅ LLM analysis complete.")
        context["analysis_result"] = result_json
        return context

    except json.JSONDecodeError as e:
        print("❌ JSON parsing failed again.")
        print("🪵 Cleaned String:", clean_json_str[:200] + "...")
        context["analysis_result"] = None
        return context