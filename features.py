import sys
from numpy import rint
import pandas as pd
import pandas_ta as ta
import os

def generate_features(symbol="APPL"):
    base_dir = os.path.dirname(os.path.abspath(__file__))    
    input_path = os.path.join(base_dir, "data", f"{symbol.lower()}_raw.csv")
    spy_path = os.path.join(base_dir, "data", "spy_raw.csv")

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run data_load.py first.")
        return
    
    if not os.path.exists(spy_path):
        print("SPY data missing. Initializing emergency fetch...")
    
    df = pd.read_csv(input_path)
    spy_df = pd.read_csv(spy_path)

    #f.columns = [c.lower() for c in df.columns]
    df.columns = [c.lower() for c in df.columns]
    spy_df.columns = [c.lower() for c in spy_df.columns]

    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.date
    spy_df['timestamp'] = pd.to_datetime(spy_df['timestamp']).dt.date

    #Calculate Base Returns
    df['returns'] = df['close'].pct_change()
    spy_df['spy_returns'] = spy_df['close'].pct_change()
    
    #Merge Market Context 
    df = pd.merge(df, spy_df[['timestamp', 'spy_returns']], on='timestamp', how='left')
    df['spy_returns'] = df['spy_returns'].ffill().bfill() # Clean missing data

    # Relative Strength
    df['relative_strength'] = (df['returns'] - df['spy_returns']).fillna(0)

    #Indicators
    df['rsi'] = ta.rsi(df['close'], length=14)
    df['sma_20'] = ta.sma(df['close'], length=20)
    df['sma_50'] = ta.sma(df['close'], length=50)
    df['vol_change'] = df['volume'].pct_change()

    # Golden Cross: 1 if 20-day is above 50-day SMA
    df['golden_cross'] = (df['sma_20'] > df['sma_50']).astype(int)

    # Overnight Gap: Percent difference between today's open and yesterday's close
    df['gap'] = (df['open'] - df['close'].shift(1)) / df['close'].shift(1)
    
    # Bollinger Bands
    bbands = ta.bbands(df['close'], length=20, std=2)
    df = pd.concat([df, bbands], axis=1)

    #Target Variable by 0.5%
    df['Target'] = (df['close'].shift(-1) > (df['close'] * 1.002)).astype(int)

    #To see momentum of the stock, add lagged features
    for lag in range(1,4):
        df[f'rsi_lag_{lag}'] = df['rsi'].shift(lag)
        df[f'rel_strength_lag_{lag}'] = df['relative_strength'].shift(lag)
    

    df.dropna(inplace=True)

    output_path = os.path.join(base_dir, "data", f"{symbol.lower()}_processed.csv")
    df.to_csv(output_path, index=False)
    print(f"Success! Features generated: {output_path}")

if __name__ == "__main__":
    target_ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    generate_features(target_ticker)