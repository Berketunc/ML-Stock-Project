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
    
    data_dir = os.path.join(os.getcwd(), "data")
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

    print(f"Fetching data for {symbol}...")
    bars = client.get_stock_bars(request_params)
    
    # Save to CSV
    file_path = os.path.join(data_dir, f"{symbol.lower()}_raw.csv")
    bars.df.to_csv(file_path)
    print(f"Data saved to {file_path}")

    print(f"Success! Data for {symbol} saved to {file_path}")

if __name__ == "__main__":
    fetch_and_save_data("AAPL")