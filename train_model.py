import sys
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_model(symbol="AAPL"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data", f"{symbol.lower()}_processed.csv")

    df = pd.read_csv(data_path)

    #Select features (Input) and target (Prediction)
    core_features = ['RSI', 'SMA_20', 'SMA_50', 'Vol_Change', 'Daily_Range', 'Price_Pct_Change']

    # Find the specific BB names created by pandas_ta
    bbl_col = [c for c in df.columns if c.startswith('BBL')][0]
    bbu_col = [c for c in df.columns if c.startswith('BBU')][0]
    
    features = core_features + [bbl_col, bbu_col]

    X = df[features]
    y = df['Target']

    #80-20 Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(
        n_estimators = 500,
        max_depth = 10,
        min_samples_leaf = 5,
        random_state = 1,
        n_jobs = -1
        )
    
    model.fit(X_train, y_train)

    #Feature Importance
    importance = model.feature_importances_
    for name, importance in zip(features, importance):
        print(f"Feature: {name}, Importance: {importance:.4f}")

    #Calculate 
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model Accuracy: {accuracy:.2%}")

    #Save
    model_dir = os.path.join(base_dir, "model")
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    model_path = os.path.join(model_dir, f"{symbol.lower()}_model.pkl")
    joblib.dump(model, model_path)
    print(f"Brain saved to: {model_path}")
    
if __name__ == "__main__":
    target_ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    train_model(target_ticker)
    