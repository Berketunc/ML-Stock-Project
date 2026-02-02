import sys
import joblib
import pandas as pd
import os

def make_prediction(symbol="AAPL"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "model", f"{symbol.lower()}_model.pkl")
    data_path = os.path.join(base_dir, "data", f"{symbol.lower()}_processed.csv")

    if not os.path.exists(model_path):
        print("Error: No trained model found. Run train_model.py first.")
        return
    
    model = joblib.load(model_path)
    df = pd.read_csv(data_path)

    #Feature Selection
    core_features = ['rsi', 'sma_20', 'sma_50', 'vol_change', 'golden_cross', 'gap', 'spy_returns', 'relative_strength',
                     'rsi_lag_1', 'rsi_lag_2', 'rsi_lag_3',
                     'rel_strength_lag_1', 'rel_strength_lag_2', 'rel_strength_lag_3'
                     ]
    
    bbl_col = [c for c in df.columns if c.startswith('BBL')][0]
    bbu_col = [c for c in df.columns if c.startswith('BBU')][0]
    features = core_features + [bbl_col, bbu_col]

    # Get the latest row for prediction
    latest_features = df[features].tail(1)
    
    prediction = model.predict(latest_features)
    probability = model.predict_proba(latest_features)

    print(f"\n--- Prediction for {symbol} ---")
    if prediction[0] == 1:
        print(f"Direction: UP (Confidence: {probability[0][1]:.2%})")
    else:
        print(f"Direction: DOWN (Confidence: {probability[0][0]:.2%})")

if __name__ == "__main__":
    target_ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    make_prediction(target_ticker)