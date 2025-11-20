import logging
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd
import pandas_ta as ta
from hmmlearn.hmm import GaussianHMM

logger = logging.getLogger(__name__)

MODELS_DIR = Path("models/hmm")
MODELS_DIR.mkdir(parents=True, exist_ok=True)

class FeatureEngineer:
    feature_cols = ['log_ret', 'volatility', 'vol_z', 'adx', 'rsi']

    @staticmethod
    def prepare_features(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
        """Engineer base features (unscaled)."""
        df = df.copy()

        # 1. Log Returns
        df['log_ret'] = np.log(df['close'] / df['close'].shift(1))

        # 2. Realized Volatility
        df['volatility'] = df['log_ret'].rolling(window=window).std()

        # 3. Volume Z-Score
        vol_mean = df['volume'].rolling(window=window*2).mean()
        vol_std = df['volume'].rolling(window=window*2).std()
        df['vol_z'] = (df['volume'] - vol_mean) / (vol_std + 1e-8)

        # 4. ADX
        adx_df = ta.adx(df['high'], df['low'], df['close'], length=window)
        if adx_df is not None and not adx_df.empty:
            adx_col = f"ADX_{window}"
            if adx_col in adx_df.columns:
                df['adx'] = adx_df[adx_col]
            else:
                df['adx'] = adx_df.iloc[:, 0]
        else:
            df['adx'] = 0.0

        # 5. RSI
        df['rsi'] = ta.rsi(df['close'], length=window)

        # Drop NaNs created by rolling windows
        df.dropna(inplace=True)

        return df[FeatureEngineer.feature_cols]

    @staticmethod
    def scale_features(features: pd.DataFrame, mean: Optional[np.ndarray] = None, std: Optional[np.ndarray] = None):
        X = features.values.astype(float)
        if mean is None or std is None:
            mean = X.mean(axis=0)
            std = X.std(axis=0) + 1e-8
        Xs = (X - mean) / std
        return Xs, mean, std

class HMMModel:
    def __init__(self, n_components: int = 3, covariance_type: str = "diag", n_iter: int = 100):
        self.n_components = n_components
        self.covariance_type = covariance_type
        self.n_iter = n_iter
        self.model: Optional[GaussianHMM] = None
        self.is_fitted = False
        self.feature_cols = FeatureEngineer.feature_cols
        self.regime_labels: Dict[int, str] = {}
        self.scaler_mean: Optional[np.ndarray] = None
        self.scaler_std: Optional[np.ndarray] = None

    def _init_model(self, n_components: int):
        return GaussianHMM(
            n_components=n_components,
            covariance_type=self.covariance_type,
            n_iter=self.n_iter,
            random_state=42,
            verbose=False,
        )

    def _bic(self, loglik: float, n_samples: int, n_features: int, n_states: int) -> float:
        # Approximate parameter count for diag-cov HMM
        p = (n_states - 1) + n_states * n_features  # means
        p += n_states * n_features  # diag covariances
        return -2 * loglik + p * np.log(max(n_samples, 1))

    def train(self, df: pd.DataFrame, auto_k: bool = False, k_min: int = 2, k_max: int = 4, strict_k: bool = False, legacy: bool = False):
        features_raw = FeatureEngineer.prepare_features(df)
        if features_raw.empty:
            raise ValueError("Not enough data to generate features")

        X_raw = features_raw.values
        n = len(X_raw)
        if n < 200:
            raise ValueError("Need at least 200 samples after feature prep")

        # Legacy path: match original behavior (no scaling, full cov, fit on all data)
        if legacy:
            self.covariance_type = "full"
            k = self.n_components
            model = self._init_model(k)
            model.fit(X_raw)
            self.model = model
            self.scaler_mean = np.zeros(X_raw.shape[1])
            self.scaler_std = np.ones(X_raw.shape[1])
            self.is_fitted = True
            states_full = self.model.predict(X_raw)
            stats = self.get_regime_stats(features_raw, states_full)
            self.label_regimes(stats)
            stats = self.get_regime_stats(features_raw, states_full)
            diagnostics = {
                "mode": "legacy",
                "k": k,
                "loglik_train": float(self.model.score(X_raw)),
                "loglik_val": None,
                "bic": None,
                "state_counts": np.bincount(states_full, minlength=k).tolist(),
                "n_train": n,
                "n_val": 0,
            }
            return stats, diagnostics

        # Modern path
        split = int(n * 0.8)
        X_train_raw, X_val_raw = X_raw[:split], X_raw[split:]
        X_train_scaled, mean, std = FeatureEngineer.scale_features(pd.DataFrame(X_train_raw))
        X_val_scaled, _, _ = FeatureEngineer.scale_features(pd.DataFrame(X_val_raw), mean, std)

        best = None
        if strict_k:
            k_candidates = [self.n_components]
        else:
            k_candidates = range(k_min, k_max + 1) if auto_k else [self.n_components]

        for k in k_candidates:
            model = self._init_model(k)
            model.fit(X_train_scaled)
            loglik_train = model.score(X_train_scaled)
            loglik_val = model.score(X_val_scaled) if len(X_val_scaled) else np.nan
            bic = self._bic(loglik_train, len(X_train_scaled), X_train_scaled.shape[1], k)

            # Degenerate state check on train
            states_train = model.predict(X_train_scaled)
            counts = np.bincount(states_train, minlength=k)
            min_ratio = counts.min() / max(len(states_train), 1)
            if min_ratio < 0.01:
                continue

            cand = {
                "k": k,
                "model": model,
                "loglik_train": loglik_train,
                "loglik_val": loglik_val,
                "bic": bic,
                "counts": counts,
                "mean": mean,
                "std": std,
            }
            if best is None or bic < best.get("bic", float("inf")):
                best = cand

        if best is None:
            raise ValueError("No viable model: states degenerate or data too short")

        self.model = best["model"]
        self.n_components = best["k"]
        self.scaler_mean = best["mean"]
        self.scaler_std = best["std"]
        self.is_fitted = True

        # Fit stats on full scaled data with chosen scaler
        X_full_scaled, _, _ = FeatureEngineer.scale_features(pd.DataFrame(X_raw), self.scaler_mean, self.scaler_std)
        states_full = self.model.predict(X_full_scaled)
        stats = self.get_regime_stats(features_raw, states_full)
        self.label_regimes(stats)
        stats = self.get_regime_stats(features_raw, states_full)
        diagnostics = {
            "mode": "modern",
            "k": self.n_components,
            "loglik_train": best["loglik_train"],
            "loglik_val": best["loglik_val"],
            "bic": best["bic"],
            "state_counts": best["counts"].tolist(),
            "n_train": len(X_train_scaled),
            "n_val": len(X_val_scaled),
        }

        return stats, diagnostics

    def label_regimes(self, stats: Dict[int, Dict]):
        """Heuristic labeling of regimes with clearer defaults."""
        sorted_states = sorted(stats.items(), key=lambda x: x[1]['avg_return'])
        
        # Clear existing
        self.regime_labels = {}
        
        n = self.n_components
        if n == 2:
            labels = ["Bear", "Bull"]
        elif n == 3:
            labels = ["Bear", "Chop", "Bull"]
        elif n == 4:
            labels = ["Strong Bear", "Bear", "Chop", "Bull"]
        else:
            labels = ["Strong Bear", "Bear"]
            mid_count = n - 4
            for i in range(mid_count):
                labels.append(f"Chop {i+1}")
            labels.extend(["Bull", "Strong Bull"])

        for (state, _), label in zip(sorted_states, labels):
            self.regime_labels[state] = label

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model is not fitted")
        features = FeatureEngineer.prepare_features(df)
        Xs, _, _ = FeatureEngineer.scale_features(features, self.scaler_mean, self.scaler_std)
        return self.model.predict(Xs)

    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model is not fitted")
        features = FeatureEngineer.prepare_features(df)
        Xs, _, _ = FeatureEngineer.scale_features(features, self.scaler_mean, self.scaler_std)
        return self.model.predict_proba(Xs)

    def get_regime_stats(self, features: pd.DataFrame, states: np.ndarray) -> Dict[int, Dict]:
        df = features.copy()
        df['state'] = states
        
        stats = {}
        for state in range(self.n_components):
            state_data = df[df['state'] == state]
            if state_data.empty:
                stats[state] = {"count": 0}
                continue
                
            stats[state] = {
                "label": self.regime_labels.get(state, f"Regime {state}"),
                "count": len(state_data),
                "avg_return": float(state_data['log_ret'].mean()),
                "volatility": float(state_data['log_ret'].std()),
                "avg_adx": float(state_data['adx'].mean()),
                "avg_rsi": float(state_data['rsi'].mean()),
                "avg_vol_z": float(state_data['vol_z'].mean())
            }
        return stats

    def save(self, name: str):
        path = MODELS_DIR / f"{name}.pkl"
        with open(path, "wb") as f:
            pickle.dump(self, f)
        logger.info(f"Model saved to {path}")

    @staticmethod
    def load(name: str) -> 'HMMModel':
        path = MODELS_DIR / f"{name}.pkl"
        if not path.exists():
            raise FileNotFoundError(f"Model {name} not found")
        with open(path, "rb") as f:
            return pickle.load(f)
