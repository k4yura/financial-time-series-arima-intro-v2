<<<<<<< HEAD
# financial-time-series-arima-intro-v2
financial-time-series-arima-intro-v2
=======
# financial-time-series-arima-intro

**Part 1 of a 3-part workshop:** data pulling → preprocessing → stationarity checks → ARIMA scaffold

This repository is code-focused (no notebooks). Many functions are intentionally left as TODOs for students to implement.

## Structure
```
financial-time-series-arima-intro/
├── README.md
├── requirements.txt
├── data/
│   └── raw/                # auto-created by data loader
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── modeling_basics.py
│   └── utils.py
├── examples/
│   └── example_usage.py
└── tests/
    ├── test_preprocessing.py
    └── test_features.py
```

## Quickstart (developer / student)
1. Create a virtualenv and install:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\\Scripts\\activate on Windows
   pip install -r requirements.txt
   ```

2. Auto-pull SPY (last 2 years) and save CSV:
   ```bash
   python src/data_loader.py
   # -> saves to data/raw/spy.csv
   ```

3. Explore `src/` files and implement TODOs:
   - `preprocessing.py` — ADF test, differencing, train/test split
   - `feature_engineering.py` — lags, rolling features
   - `modeling_basics.py` — build & evaluate ARIMA model using statsmodels

4. Run unit tests:
   ```bash
   pytest -q
   ```

## Learning goals for Part 1
- Acquire real price series using `yfinance`
- Test for stationarity and apply appropriate transforms
- Build lag / rolling features
- Fit a basic ARIMA model (students fill the fitting code)
- Understand evaluation for time-series forecasts

## Notes
- This repo intentionally leaves major implementation points for students to implement as exercises.
- Part 2 and Part 3 (model expansion, options logic, trading simulation) will build on these foundations.
>>>>>>> d1674ba (workshop part 1 commit)
