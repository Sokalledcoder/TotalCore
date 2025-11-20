# HMM Regime Detection Walkthrough

## Overview
We have successfully integrated a Hidden Markov Model (HMM) engine into TradeCore for market regime detection. This module allows you to:
1.  **Ingest** full historical data from Binance Futures (starting 2019).
2.  **Train** HMM models to classify market states into semantic regimes (**Bull**, **Bear**, **Chop**).
3.  **Monitor** regimes in real-time via a premium Dashboard.

## New Components

### 1. HMM Dashboard
**URL**: `/hmm-dashboard`
A premium dark-mode interface to interact with the HMM engine.
-   **Controls**: Select Exchange, Symbol, Timeframe, and Number of States.
-   **Price Chart**: **Candlestick chart** with candles colored by the detected regime (Green=Bull, Red=Bear, Grey=Chop).
-   **Probability Strip**: Stacked area chart showing the probability of each regime over time.

### 2. HMM Engine (`app/services/hmm_engine.py`)
The core logic powered by `hmmlearn`.
-   **Features**:
    -   **Log Returns**: Directional movement.
    -   **Volatility**: Rolling standard deviation of returns.
    -   **Volume Z-Score**: Relative trading activity.
    -   **ADX**: Trend strength indicator.
    -   **RSI**: Momentum indicator.
-   **Auto-Labeling**: The engine automatically assigns labels (Bull, Bear, Chop) based on the average return of each state.

### 3. Data Pipeline (`app/ingestion/fetcher.py`)
-   **DuckDB**: High-performance columnar database.
-   **Full History**: Automatically fetches data from Sept 2019 for Binance BTC/USDT.

## How to Use

### Step 1: Ingest Data
Use the API to trigger a full history fetch.
```bash
# This will fetch from 2019-09-08 to now
curl -X POST http://localhost:8000/api/data-jobs -d '{"exchange": "binance", "symbol": "BTC/USDT", "timeframe": "15m"}'
```

### Step 2: Train Model
Go to the **HMM Lab** (`/hmm-dashboard`).
1.  Select **Binance**, **BTC/USDT**, **15m**.
2.  Set **States** to 3.
3.  Click **Train Model**.
4.  View the "Regime Stats" card to see the characteristics of each state.

### Step 3: Analyze
The charts will automatically refresh.
-   **Visuals**: Look for Green candles (Bull) vs Red candles (Bear).
-   **Stats**: Check the RSI and ADX values for each regime to confirm their nature.

## Verification Results
We ran a verification script (`scripts/verify_hmm.py`) on a sample dataset.
-   **Training**: Successfully trained a 3-state Gaussian HMM.
-   **Labels**: Correctly assigned "Bull", "Bear", "Chop".
-   **Inference**: Probabilities correctly sum to 1.0.

### Sample Output
```json
{
  "0": {
    "label": "Bull",
    "avg_return": 0.0012,
    "avg_rsi": 41.10
  },
  "1": {
    "label": "Chop",
    "avg_return": 0.0001,
    "avg_rsi": 40.67
  },
  "2": {
    "label": "Bear",
    "avg_return": -0.0004,
    "avg_rsi": 42.76
  }
}
```
