import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import os

def generate_visuals(symbol="nvda"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load data and model
    df = pd.read_csv(os.path.join(base_dir, "data", f"{symbol}_processed.csv"))
    model = joblib.load(os.path.join(base_dir, "model", f"{symbol}_model.pkl"))
    
    #Correlation Heatmap 
    features = [col for col in df.columns if 'rsi' in col or 'rel' in col or 'vol' in col or 'spy' in col]
    plt.figure(figsize=(12, 8))
    sns.heatmap(df[features].corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(f'Feature Correlation Matrix - {symbol.upper()}')
    plt.savefig('correlation_heatmap.png')
    print("📈 Correlation heatmap saved as correlation_heatmap.png")

    #Feature Importance Plot
    #Extract importance from XGBoost
    importance_df = pd.DataFrame({
        'Feature': model.get_booster().feature_names,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Importance', y='Feature', data=importance_df, palette='viridis')
    plt.title(f'XGBoost Feature Importance - {symbol.upper()}')
    plt.tight_layout()
    plt.savefig('feature_importance.png')
    print("📊 Feature importance plot saved as feature_importance.png")

if __name__ == "__main__":
    generate_visuals("nvda")