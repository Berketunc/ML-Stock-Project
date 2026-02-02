import sys
import os
import pandas as pd
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

load_dotenv()

def fetch_and_save_data(symbol="AAPL"):
    #GET KEYS
    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")

    base_dir = os.path.dirname(os.path.abspath(__file__))    
    data_dir = os.path.join(base_dir, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    client = StockHistoricalDataClient(api_key, secret_key)

    request_params = StockBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=TimeFrame.Day,
        start=datetime.now() - timedelta(days=730),
        end=datetime.now(),
        feed="iex"
    )

    for ticker in [symbol, "SPY"]:
        print(f"Fetching data for {ticker}...")
        request_params = StockBarsRequest(
            symbol_or_symbols=[ticker],
            timeframe=TimeFrame.Day,
            start=datetime.now() - timedelta(days=730),
            feed='iex'
        )

    print(f"Fetching data for {symbol}...")
    bars = client.get_stock_bars(request_params)
    
    # Save to CSV
    file_path = os.path.join(data_dir, f"{symbol.lower()}_raw.csv")
    bars.df.to_csv(file_path)
    print(f"Data saved to {file_path}")

    print(f"Success! Data for {symbol} saved to {file_path}")

if __name__ == "__main__":
    target_ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    fetch_and_save_data(target_ticker)

    if not os.path.exists("data/spy_raw.csv") or target_ticker == "SPY":
        fetch_and_save_data("SPY")