"""
Minimal example: show the pipeline (mostly scaffold).

This script demonstrates:
- auto-pull SPY via data_loader (saved to data/raw/spy.csv)
- load CSV and create a simple pipeline of preprocessing -> features -> model skeleton

Students: flesh out and run end-to-end by implementing TODOs.
"""

from src.data_loader import default_pull_and_save
from pathlib import Path
import pandas as pd
from src.preprocessing import make_stationary, train_test_split_ts
from src.feature_engineering import create_lag_features, create_rolling_features
from src.modeling_basics import select_arima_order, fit_arima, forecast_and_evaluate
from src.utils import setup_basic_logging
import logging

setup_basic_logging()
logger = logging.getLogger(__name__)

def run_demo():
    # Step 1: Download (auto) and save SPY
    df = default_pull_and_save()  # saves to data/raw/spy.csv
    # Use 'Adj Close' for modeling
    series = df["Adj Close"].copy()
    # Step 2: Stationarize (student must implement improved logic)
    stationary_series, d = make_stationary(series)
    logger.info(f"Applied differencing order d={d}, resulting length {len(stationary_series)}")
    # Step 3: Feature engineering (students may augment)
    fe = create_lag_features(stationary_series, lags=[1,2,3])
    fe2 = create_rolling_features(stationary_series, windows=[5,10], funcs=["mean","std"])
    # Step 4: Train/test split
    train, test = train_test_split_ts(stationary_series, test_size=0.2)
    # Step 5: Model selection, fit, forecast (students fill improvements)
    order = select_arima_order(train)
    fitted = fit_arima(train, order)
    res = forecast_and_evaluate(fitted, steps=len(test), actual=test)
    logger.info(f"Forecast RMSE: {res.get('rmse')}, MAPE: {res.get('mape')}")
    print("Forecast head:")
    print(res["forecast"].head())

if __name__ == "__main__":
    run_demo()
