# HMM Optimization Plan

This document outlines the current state of our HMM implementation and proposes specific optimizations based on financial time-series research.

## 1. Feature Engineering

### Current Approach
*   **Features**:
    *   `log_ret`: Log Returns (Stationary, small scale ~0.001)
    *   `volatility`: Rolling Std Dev (Stationary, small scale)
    *   `vol_z`: Volume Z-Score (Stationary, scale ~ -3 to +3)
    *   `adx`: Trend Strength (Bounded 0-100, non-stationary trends)
    *   `rsi`: Momentum (Bounded 0-100, non-stationary trends)
*   **Issue**:
    *   **Scale Imbalance**: HMMs using Gaussian emissions are sensitive to scale. `log_ret` is ~0.001 while `rsi` is ~50. The model will be dominated by `rsi` and ignore returns, effectively becoming just an "RSI clustering" algorithm.
    *   **Distribution**: `hmmlearn` assumes features follow a Gaussian (Normal) distribution. `rsi` and `adx` are bounded and often skewed, violating this assumption.

### Optimal Approach
*   **Z-Score Scaling**: Apply `StandardScaler` to **ALL** features before training.
    *   Formula: $z = \frac{x - \mu}{\sigma}$
    *   **Why**: This brings all features to the same scale (mean=0, std=1), ensuring the HMM weighs them equally.
*   **Transformations**:
    *   Instead of raw `rsi`, use `rsi_z` (Z-scored RSI) or `rsi_diff` (Change in RSI) to better approximate a Gaussian distribution.
    *   Ensure all inputs are stationary (statistical properties don't change over time).

## 2. Model Architecture

### Current Approach
*   **Covariance**: Defaults to `"diag"` (Diagonal) in our code.
*   **State Selection**: User manually selects $K$ (e.g., 3 states).

### Optimal Approach
*   **Covariance Type**: **Keep `"diag"`**.
    *   **Why**: Financial data is noisy. A "full" covariance matrix requires estimating $N^2$ parameters per state (correlations between all features). "Diag" only estimates $N$ parameters (variances). "Diag" is less prone to overfitting and more stable for regime detection.
*   **Auto-K Selection (BIC)**:
    *   **Why**: Guessing the number of regimes is hard. Does the market have 2 (Bull/Bear), 3 (+Chop), or 4 (+Crash)?
    *   **Method**: Train models with $K=2, 3, 4, 5$ and calculate the **Bayesian Information Criterion (BIC)**.
    *   **Goal**: Select the $K$ that minimizes BIC. This mathematically balances model fit (Likelihood) vs. complexity (Penalty for more parameters).

## 3. Training Stability

### Current Approach
*   **Initialization**: Single training run (`model.fit`).
*   **Issue**: HMM training uses the EM (Expectation-Maximization) algorithm, which is guaranteed to improve likelihood but **not** guaranteed to find the global optimum. It often gets stuck in local optima depending on random initialization.

### Optimal Approach
*   **Multiple Random Restarts**:
    *   **Method**: Train the model 5-10 times with different random seeds.
    *   **Selection**: Keep the model with the highest **Log-Likelihood**.
    *   **Why**: This ensures we find the "best" definition of regimes and prevents the model from flipping definitions (e.g., sometimes State 0 is Bull, sometimes it's Bear) purely due to bad luck.

## 4. Data Granularity

### Current Approach
*   **Data**: 1-minute candles.
*   **Issue**: 1-minute data is dominated by "microstructure noise" (bid-ask bounce, small order flows) rather than true structural regimes.

### Optimal Approach
*   **Resampling**:
    *   **Method**: Downsample 1m data to **15m**, **1h**, or **4h** before training.
    *   **Why**: Regimes like "Bull Trend" or "Choppy" usually persist for hours or days. Higher timeframes filter out noise and reveal these structural states more clearly. The HMM will be more robust and less "jittery".

## Summary of Proposed Changes

| Component | Current | Proposed | Benefit |
| :--- | :--- | :--- | :--- |
| **Scaling** | None (Raw values) | **Z-Score (StandardScaler)** | Prevents RSI/ADX from dominating the model. |
| **K-Selection** | Manual (User input) | **Auto-BIC** | Automatically finds the true number of market regimes. |
| **Training** | Single Run | **Multi-Restart (Best of N)** | Prevents bad models due to unlucky initialization. |
| **Features** | Raw RSI/ADX | **Transformed/Scaled** | Better fits Gaussian assumption of HMM. |

---
**Recommendation**: We should implement **Z-Score Scaling** and **Multi-Restart Training** immediately as they are critical for correctness. **Auto-BIC** can be added as an optional "Auto-Tune" feature.
