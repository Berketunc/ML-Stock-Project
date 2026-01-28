import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient

load_dotenv()

api_key = os.getenv("ALPACA_API_KEY")
api_secret = os.getenv("ALPACA_API_SECRET")

if not api_key or not api_secret:
    print("API key and secret must be set in environment variables.")
else:
    try:
        client = TradingClient(api_key, api_secret, paper=True)
        account = client.get_account()
        print(f"✅ Success! Connected to account: {account.account_number}")
        print(f"Current Equity: ${account.equity}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")