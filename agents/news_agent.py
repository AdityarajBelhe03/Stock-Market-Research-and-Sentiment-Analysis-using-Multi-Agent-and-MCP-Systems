import requests
import os
from datetime import datetime, timedelta

def run_news_agent(context: dict, config: dict) -> dict:
    print(f"🗞️ [NewsAgent] Fetching news for {context['symbol']}...")

    symbol = context["symbol"]
    api_key = config["finnhub_api_key"]

    # Date range: past 7 days
    to_date = datetime.today().date()
    from_date = to_date - timedelta(days=7)

    url = (
        f"https://finnhub.io/api/v1/company-news"
        f"?symbol={symbol}&from={from_date}&to={to_date}&token={api_key}"
    )

    res = requests.get(url)
    if res.status_code != 200:
        print("❌ Failed to fetch news.")
        context["headlines"] = []
        return context

    articles = res.json()
    if not articles:
        print("⚠️ No news found for this symbol.")
        context["headlines"] = []
        return context

    # Extract top 10 headlines
    headlines = [article["headline"] for article in articles if "headline" in article][:10]

    print(f"✅ Retrieved {len(headlines)} headlines.")
    context["headlines"] = headlines
    return context