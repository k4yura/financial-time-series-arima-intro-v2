"""
Feature engineering helpers for time-series:
- create_lag_features
- create_rolling_features

Students should implement core logic (TODOs) while basic structure and docstrings are provided.
"""

import pandas as pd
from typing import List
import logging

logger = logging.getLogger(__name__)

def create_lag_features(series: pd.Series, lags: List[int]) -> pd.DataFrame:
    """
    Create lagged features for a given series.

    Parameters:
    - series: pd.Series with datetime index
    - lags: list of integers e.g., [1,2,3,5]

    Returns:
    - DataFrame where each column is 'lag_{k}' containing series shifted by k
    """
    df = pd.DataFrame({"y": series})
    for k in lags:
        # TODO (student): consider how to name and handle NaNs produced by shift
        df[f"lag_{k}"] = series.shift(k)
    # Optionally drop rows with NaN values introduced by lagging
    return df

def create_rolling_features(series: pd.Series, windows: List[int], funcs: List[str] = None) -> pd.DataFrame:
    """
    Create rolling window features (mean, std, min, max by default).

    Parameters:
    - series: pd.Series
    - windows: list of integers for window sizes
    - funcs: list of strings naming rolling functions ('mean','std','min','max')

    Returns:
    - DataFrame with columns like 'roll_{w}_mean'
    """
    if funcs is None:
        funcs = ["mean", "std"]
    df = pd.DataFrame({"y": series})
    for w in windows:
        roll = series.rolling(window=w)
        for f in funcs:
            col = f"roll_{w}_{f}"
            # TODO (student): verify that requested func is supported or implement mapping
            if f == "mean":
                df[col] = roll.mean()
            elif f == "std":
                df[col] = roll.std()
            elif f == "min":
                df[col] = roll.min()
            elif f == "max":
                df[col] = roll.max()
            else:
                # for advanced usage, students may implement custom functions
                logger.warning(f"Unknown rolling function: {f} (skipping)")
                df[col] = roll.mean()  # default fallback
    return df
