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

    #Target Variable
    df['Target'] = (df['close'].shift(-1) > df['close']).astype(int)

    df.dropna(inplace=True)

    output_path = os.path.join(base_dir, "data", f"{symbol.lower()}_processed.csv")
    df.to_csv(output_path, index=False)
    print(f"Success! Features generated: {output_path}")

if __name__ == "__main__":
    generate_features("AAPL")