from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import re

# Load FinBERT-based sentiment pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")

def clean_text(text):
    """Lowercase and remove extra whitespace."""
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def run_sentiment_agent(context: dict) -> dict:
    print("🧠 [SentimentAgent] Using FinBERT for financial sentiment analysis...")

    headlines = context.get("headlines", [])
    if not headlines:
        print("⚠️ No headlines found in context.")
        context["sentiment_summary"] = None
        return context

    results = []
    score_map = {"positive": 1, "negative": -1, "neutral": 0}
    sentiment_total = 0

    for headline in headlines:
        cleaned = clean_text(headline)
        result = sentiment_pipeline(cleaned[:512])[0]
        label = result['label'].lower()  # FinBERT returns lowercase labels
        score = result['score']

        results.append({
            "headline": headline,
            "sentiment": label.upper(),
            "confidence": round(score, 3)
        })

        sentiment_total += score_map.get(label, 0)

    overall_sentiment = (
        "POSITIVE" if sentiment_total > 1 else
        "NEGATIVE" if sentiment_total < -1 else
        "NEUTRAL"
    )

    context["sentiment_summary"] = {
        "per_headline": results,
        "overall": overall_sentiment
    }

    print(f"✅ Overall Financial Sentiment: {overall_sentiment}")
    return context