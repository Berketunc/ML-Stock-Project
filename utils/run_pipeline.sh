#!/bin/bash

cd "$(dirname "$0")/.."

# 1. Activate the virtual environment
source venv/bin/activate

TICKER=${1:-AAPL}

echo "Starting ML Stock Pipeline for $TICKER"

# 2. Run Data Loader
python3 data_load.py "$TICKER"
if [ $? -ne 0 ]; then echo "Data load failed!"; exit 1; fi

# 3. Run Feature Engineering
python3 features.py "$TICKER"
if [ $? -ne 0 ]; then echo "Feature engineering failed!"; exit 1; fi

# 4. Run Model Training
python3 train_model.py "$TICKER"
if [ $? -ne 0 ]; then echo "Model training failed!"; exit 1; fi

# 5. Run Prediction
python3 Prediction.py "$TICKER"
if [ $? -ne 0 ]; then echo "Prediction failed!"; exit 1; fi

echo "Pipeline complete for $TICKER!"
