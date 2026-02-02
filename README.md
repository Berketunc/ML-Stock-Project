# 📈 ML Stock Trend Predictor

An automated machine learning pipeline that predicts short-term stock price movements using **XGBoost**. This project automates the entire process from fetching live market data to generating high-confidence trade signals.

# Features
-Full Automation: A single Bash script runs the entire pipeline from data fetching to prediction.

-Advanced ML: Swapped standard Random Forest for XGBoost to handle market noise.

-Market Context: Incorporates S&P 500 (SPY) relative strength to filter out "market-wide" noise.

-Technical Indicators: Uses RSI, SMA Crossovers (Golden Cross), Bollinger Bands, and Volume analysis via pandas-ta.

-Dynamic Tickers: Supports any stock ticker available on Alpaca (e.g., AAPL, NVDA, TSLA).


# Project Structure
* `data/` - Storage for raw and processed CSV files.
* `model/` - Serialized XGBoost models (.pkl).
* `utils/run_pipeline.sh` - The master bash script to execute the pipeline.
* `data_load.py` - Ingests data from Alpaca API.
* `features.py` - Handles technical analysis and data merging.
* `train_model.py` - Executes XGBoost training and feature importance analysis.
* `Prediction.py` - Generates the final prediction for the latest market data.

# Setup & Installation
1. Clone the repo

2. Set up Environment (Used ALPACA APIs)

3. Install dependencies 


python3 -m venv venv


source venv/bin/activate


pip install -r requirements.txt

4. Script
./utils/run_pipeline.sh <TICKER>


The default is set to 'AAPL' 


# 📊 Sample Output (AAPL)
Accuracy: 48.89%


Prediction: DOWN


Confidence: 95.40%


Top Driver: Upper Bollinger Band (18.8%) — Indicates an overbought state.

# 📊 Sample Output (NVDA)
Accuracy: 53.33%


Prediction: DOWN


Confidence: 93.79%


Key Drivers: RSI (14.2%), Gap/Overnight Sentiment (13.5%), SMA 20 (13.4%)

# ⚖️ Disclaimer
This project is for educational purposes only. This is not financial advice. Trading stocks involves significant risk, and this model is a simplified demonstration of machine learning application.

# Future Roadmap:
Hyperparameter Tuning: Implement GridSearchCV to optimize XGBoost max_depth and learning_rate.

Macro Integration: Add interest rate (FED) or sentiment analysis from financial news.

Backtesting Suite: Develop a script to simulate historical trades based on model signals.
