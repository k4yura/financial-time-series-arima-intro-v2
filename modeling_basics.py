"""
Modeling basics: ARIMA scaffold using statsmodels.

Contains:
- function to select order (student TODO: implement heuristics or use grid search)
- function to fit ARIMA (students implement main fit and error handling)
- function to forecast and evaluate (RMSE/MAPE)

Important:
- This file intentionally leaves core parts for students to implement for learning.
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

def select_arima_order(series: pd.Series, max_p=3, max_d=2, max_q=3) -> Tuple[int,int,int]:
    """
    Very small helper to select ARIMA order.
    Student TODO:
    - Implement AIC/BIC based grid search (or use pmdarima in later parts)
    - Return (p,d,q)

    Current naive default returns (1, d, 1) where d is 0 or 1 based on simple ADF check.
    """
    # TODO (student): implement grid search over (p,d,q) and pick best AIC/BIC
    # Placeholder:
    d = 0
    # quick ADF check - student may reuse preprocessing.adf_test
    try:
        from src.preprocessing import adf_test
        pval = adf_test(series)["pvalue"]
        if pval >= 0.05:
            d = 1
    except Exception:
        d = 1
    return (1, d, 1)

def fit_arima(series: pd.Series, order: Tuple[int,int,int], enforce_stationarity=False, enforce_invertibility=False):
    """
    Fit an ARIMA model to `series` using statsmodels.

    Parameters:
    - series: pd.Series (training series)
    - order: (p,d,q)
    - enforce_stationarity, enforce_invertibility: passed to statsmodels ARIMA constructor

    Returns:
    - fitted_model (statsmodels ARIMAResults)
    """
    # TODO (student): add robust error handling, warnings, exogenous support, and parameter tuning
    logger.info(f"Fitting ARIMA{order} to series of length {len(series)}")
    # Students will implement more careful differencing and validation
    model = ARIMA(series, order=order, enforce_stationarity=enforce_stationarity,
                  enforce_invertibility=enforce_invertibility)
    fitted = model.fit()
    return fitted

def forecast_and_evaluate(fitted_model, steps: int, actual: pd.Series = None) -> dict:
    """
    Forecast `steps` ahead and optionally compute evaluation metrics against `actual`.

    Returns:
    dict {
        'forecast': pd.Series,
        'rmse': float or None,
        'mape': float or None
    }

    Student TODO:
    - implement prediction intervals
    - implement walk-forward/backtesting evaluation
    """
    pred = fitted_model.forecast(steps=steps)
    result = {"forecast": pred}
    if actual is not None:
        # align lengths
        act = actual.iloc[:len(pred)]
        rmse = np.sqrt(((pred - act) ** 2).mean())
        mape = (np.abs((act - pred) / act)).replace([np.inf, -np.inf], np.nan).dropna().mean()
        result["rmse"] = float(rmse)
        result["mape"] = float(mape)
    else:
        result["rmse"] = None
        result["mape"] = None
    return result
