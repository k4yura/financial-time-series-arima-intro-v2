"""
Preprocessing helpers: stationarity tests, differencing, splitting.

Students must implement the TODOs where main logic is required.

Functions:
- adf_test(series): runs Augmented Dickey-Fuller and returns dict of results
- make_stationary(series, max_diff=2): attempts differencing until stationary (student implements)
- train_test_split_ts(series, test_size): time-series aware split
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from typing import Tuple, Dict
import logging

logger = logging.getLogger(__name__)

def adf_test(series: pd.Series, autolag="AIC") -> Dict:
    """
    Run Augmented Dickey-Fuller test and return a dict with key statistics.

    Returns:
    {
        'adf_stat': float,
        'pvalue': float,
        'usedlag': int,
        'nobs': int,
        'critical_values': dict,
        'icbest': float or None
    }
    """
    res = adfuller(series.dropna(), autolag=autolag)
    output = {
        "adf_stat": res[0],
        "pvalue": res[1],
        "usedlag": res[2],
        "nobs": res[3],
        "critical_values": res[4],
        "icbest": res[5] if len(res) > 5 else None,
    }
    return output

def make_stationary(series: pd.Series, max_diff: int = 2, alpha: float = 0.05) -> Tuple[pd.Series, int]:
    """
    Attempt to make the series stationary by differencing up to max_diff times.
    Returns (stationary_series, d) where d is the differencing order applied.

    Student TODOs:
    - Run adf_test and decide whether to difference.
    - Try seasonal differencing if needed (optional)
    - Keep track of how many differences applied.
    """
    # Starter naive implementation: keep differencing until ADF pvalue < alpha or max_diff reached.
    s = series.copy().dropna()
    d = 0
    # TODO (student): improve stationarity detection logic (e.g., trend removal, seasonal diff)
    for i in range(max_diff + 1):
        test = adf_test(s)
        p = test["pvalue"]
        logger.info(f"ADF test at d={d}: p={p:.4f}")
        if p < alpha:
            return s, d
        # difference once
        s = s.diff().dropna()
        d += 1
    # Return last (even if not strictly stationary)
    return s, d

def train_test_split_ts(series: pd.Series, test_size: float = 0.2) -> Tuple[pd.Series, pd.Series]:
    """
    Time-series aware train/test split.

    Parameters:
    - series: pandas Series or DataFrame with index sorted ascending
    - test_size: fraction or integer
      - if 0 < test_size < 1 -> fraction used for test
      - if test_size >= 1 -> interpreted as number of samples in test set

    Returns (train, test)
    """
    if isinstance(test_size, float) and 0 < test_size < 1:
        n_test = int(len(series) * test_size)
    else:
        n_test = int(test_size)
    n_train = len(series) - n_test
    train = series.iloc[:n_train]
    test = series.iloc[n_train:]
    return train, test
