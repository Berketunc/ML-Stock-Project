import sys
import pandas as pd
import pandas_ta as ta
import os

def generate_features(symbol="APPL"):
    base_dir = os.path.dirname(os.path.abspath(__file__))    
    input_path = os.path.join(base_dir, "data", f"{symbol.lower()}_raw.csv")

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run data_load.py first.")
        return
    
    df = pd.read_csv(input_path)

    #Indicators
    df['RSI'] = ta.rsi(df['close'], length=14)
    df['SMA_20'] = ta.sma(df['close'], length=20)
    df['SMA_50'] = ta.sma(df['close'], length=50)
    df['Vol_Change'] = df['volume'].pct_change()

    # Golden Cross: 1 if 20-day is above 50-day SMA
    df['Golden_Cross'] = (df['SMA_20'] > df['SMA_50']).astype(int)

    # Overnight Gap: Percent difference between today's open and yesterday's close
    df['Gap'] = (df['open'] - df['close'].shift(1)) / df['close'].shift(1)
    
    # Bollinger Bands
    bbands = ta.bbands(df['close'], length=20, std=2)
    df = pd.concat([df, bbands], axis=1)

    #Target Variable by 0.5%
    df['Target'] = (df['close'].shift(-1) > (df['close'] * 1.005)).astype(int)

    #To see momentum of the stock, add lagged features
    for lag in [1, 2, 3]:
        df[f'Close_Lag_{lag}'] = df['close'].shift(lag)
        df[f'RSI_Lag_{lag}'] = df['RSI'].shift(lag)
    

    df.dropna(inplace=True)

    output_path = os.path.join(base_dir, "data", f"{symbol.lower()}_processed.csv")
    df.to_csv(output_path, index=False)
    print(f"Success! Features generated: {output_path}")

if __name__ == "__main__":
    target_ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    generate_features(target_ticker)