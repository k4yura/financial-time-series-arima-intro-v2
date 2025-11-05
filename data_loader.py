"""
Data loader using yfinance.

Behavior:
- If run as a script with no args: downloads SPY for the last 2 years and saves to data/raw/spy.csv
- Exposes function `load_price_data(ticker, start, end, save_path=None)` that downloads and returns OHLCV DataFrame

Students: fill the data cleaning TODOs if desired (e.g., handling missing data, resampling).
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from src.utils import save_df_csv, ensure_dir, setup_basic_logging
import logging

setup_basic_logging()
logger = logging.getLogger(__name__)

DEFAULT_SAVE_DIR = Path.cwd() / "data" / "raw"
DEFAULT_TICKER = "SPY"

def load_price_data(ticker: str, start: str, end: str, save_path: str = None) -> pd.DataFrame:
    """
    Download price data via yfinance.

    Parameters
    ----------
    ticker : str
        Ticker symbol to download (e.g., "SPY")
    start : str
        Start date in YYYY-MM-DD
    end : str
        End date in YYYY-MM-DD
    save_path : str or None
        If provided, save the CSV to this path.

    Returns
    -------
    pd.DataFrame
        DataFrame with datetime index and columns ['Open','High','Low','Close','Adj Close','Volume']
    """
    logger.info(f"Downloading {ticker} from {start} to {end}")
    df = yf.download(ticker, start=start, end=end, progress=False)

    # yfinance returns index as DatetimeIndex — keep it explicit
    df.index = pd.to_datetime(df.index)

    # TODO (student): perform any cleaning here
    # Examples:
    # - forward/backfill missing days
    # - resample to business day frequency
    # - compute returns or log-returns if desired
    # - drop rows with NaNs or impute

    if save_path:
        save_path = Path(save_path)
        ensure_dir(save_path.parent.as_posix())
        df.to_csv(save_path)
        logger.info(f"Saved raw data to {save_path}")

    return df

def default_pull_and_save(ticker: str = DEFAULT_TICKER, years: int = 2):
    """
    Convenience function: pull the last `years` years for `ticker` and save to data/raw/{ticker_lower}.csv
    """
    end = datetime.today().date()
    start = end - timedelta(days=365 * years)
    save_path = DEFAULT_SAVE_DIR / f"{ticker.lower()}.csv"
    ensure_dir(DEFAULT_SAVE_DIR.as_posix())
    df = load_price_data(ticker, start.isoformat(), end.isoformat(), save_path=save_path)
    return df

if __name__ == "__main__":
    # Auto behavior chosen: pull SPY for last 2 years and save
    logger.info("Auto-running default_pull_and_save()")
    df = default_pull_and_save()
    logger.info(f"Downloaded {len(df)} rows: head:\n{df.head()}")
    print("Saved to:", (DEFAULT_SAVE_DIR / f"{DEFAULT_TICKER.lower()}.csv").as_posix())
