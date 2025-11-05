"""
Utility functions: file IO helpers, simple logging helpers.
Keep light-weight so tests can run quickly.
"""

from pathlib import Path
import pandas as pd
import logging
import os

LOG_FORMAT = "%(asctime)s %(levelname)s: %(message)s"

def setup_basic_logging(level=logging.INFO):
    logging.basicConfig(format=LOG_FORMAT, level=level)

def ensure_dir(path: str):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def save_df_csv(df: pd.DataFrame, path: str, index=True):
    """
    Save DataFrame to CSV. Overwrites existing files.
    """
    ensure_dir(Path(path).parent.as_posix())
    df.to_csv(path, index=index)

def load_df_csv(path: str):
    """
    Return a pandas DataFrame loaded from CSV path.
    """
    return pd.read_csv(path, parse_dates=True, index_col=None)
