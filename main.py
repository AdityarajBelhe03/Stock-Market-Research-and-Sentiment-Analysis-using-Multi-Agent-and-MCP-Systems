import json
from utils.helpers import load_config
from agents.data_agent import run_data_agent
from agents.news_agent import run_news_agent
from agents.sentiment_agent import run_sentiment_agent
from agents.analyzer_agent import run_analyzer_agent
from agents.dashboard_agent import run_dashboard_agent

def initialize_context():
    config = load_config()

    print("\n💬 Welcome to Stock AI Analyst")
    user_symbol = input(f"Enter stock symbol [{config['default_symbol']}]: ") or config['default_symbol']
    user_query = input(f"Enter your stock-related question:\n→ ") or config['default_user_query']

    context = {
        "symbol": user_symbol.upper(),
        "user_query": user_query
    }

    print("\n✅ Context Initialized:")
    print(f"  Symbol: {context['symbol']}")
    print(f"  User Question: {context['user_query']}\n")

    return context, config

# ✅ Main entry point
if __name__ == "__main__":
    context, config = initialize_context()
    context = run_data_agent(context, config)
    context = run_news_agent(context, config)
    context = run_sentiment_agent(context)
    context = run_analyzer_agent(context, config)
    print("\n📊 Final Analysis Result:")
    print(json.dumps(context["analysis_result"], indent=2))

    context = run_dashboard_agent(context)
    # We will pass `context` to the first agent next (DataAgent)