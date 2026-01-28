import os
import pandas as pd
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

load_dotenv()

def fetch_and_save_data(symbol="AAPL"):
    client = StockHistoricalDataClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"))

    request_params = StockBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=TimeFrame.Day,
        start=datetime.now() - timedelta(days=730),
        end=datetime.now(),
        feed="iex"
    )

    print(f"Fetching data for {symbol}...")
    bars = client.get_stock_bars(request_params)
    bars.df.to_csv(f"{symbol}_data.csv")
    print(f"Data for {symbol} saved to {symbol}_data.csv")

if __name__ == "__main__":
    fetch_and_save_data("AAPL")