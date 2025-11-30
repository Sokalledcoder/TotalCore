from __future__ import annotations

import importlib
import logging
from dataclasses import dataclass
from typing import Dict, Any, Protocol, List

import numpy as np
import pandas as pd

from app.db import db
from app.models import BacktestDataRef
from app.backtests.registry import get_strategy_spec

logger = logging.getLogger(__name__)


@dataclass
class BacktestResult:
    engine: str
    strategy_id: str
    params: Dict[str, Any]
    equity_curve: pd.Series
    returns: pd.Series
    trades: pd.DataFrame
    metrics: Dict[str, Any]
    raw: Any
    price: pd.DataFrame
    indicators: Dict[str, pd.Series]


class EngineAdapter(Protocol):
    def run(self, strategy_id: str, params: Dict[str, Any], data: BacktestDataRef, cv_config: Dict[str, Any]) -> BacktestResult:
        ...


def _load_ohlcv(data: BacktestDataRef) -> Dict[str, pd.DataFrame]:
    frames: Dict[str, pd.DataFrame] = {}
    for symbol in data.symbols:
        symbol_norm = _normalize_symbol(data.exchange, symbol)
        df_raw = db.get_market_data(
            exchange=data.exchange,
            symbol=symbol_norm,
            timeframe=data.timeframe,
            start_date=data.start,
            end_date=data.end,
        )
        if data.limit and not df_raw.empty:
            df_raw = df_raw.tail(data.limit)
        if df_raw.empty:
            raise ValueError(f"No data for {data.exchange} {symbol_norm} {data.timeframe}")

        # Re-materialize as fully-owned, contiguous numpy buffers to avoid read-only Arrow
        df_raw = df_raw[["timestamp", "open", "high", "low", "close", "volume"]].copy()
        ts = pd.to_datetime(df_raw["timestamp"].to_numpy(copy=True), utc=True)
        mat = {
            "Open": np.ascontiguousarray(df_raw["open"].to_numpy(copy=True), dtype="float64"),
            "High": np.ascontiguousarray(df_raw["high"].to_numpy(copy=True), dtype="float64"),
            "Low": np.ascontiguousarray(df_raw["low"].to_numpy(copy=True), dtype="float64"),
            "Close": np.ascontiguousarray(df_raw["close"].to_numpy(copy=True), dtype="float64"),
            "Volume": np.ascontiguousarray(df_raw["volume"].to_numpy(copy=True), dtype="float64"),
        }
        df = pd.DataFrame(mat, index=ts)
        frames[symbol_norm] = df
    return frames


def _normalize_symbol(exchange: str, symbol: str) -> str:
    """Normalize user-entered symbols to match stored symbols."""
    s = symbol.strip().upper()
    if exchange.lower() == "binance":
        # Common user input is BTC/USD but DB stores BTC/USDT
        if s.endswith("/USD") and not s.endswith("/USDT"):
            base = s[:-4]
            s = f"{base}/USDT"
    return s


class BacktestingPyAdapter:
    def __init__(self) -> None:
        self._mod = None

    def _ensure_imports(self):
        if self._mod:
            return
        try:
            self._mod = importlib.import_module("backtesting")
        except ModuleNotFoundError as exc:  # pragma: no cover - import-time guard
            raise RuntimeError("backtesting.py is not installed. pip install backtesting") from exc

    def _build_strategy(self, strategy_id: str):
        self._ensure_imports()
        Backtest = self._mod.Backtest  # noqa: N806
        Strategy = self._mod.Strategy  # noqa: N806
        bt_lib = importlib.import_module("backtesting.lib")
        bt_test = importlib.import_module("backtesting.test")
        self._fractional_backtest = getattr(bt_lib, "FractionalBacktest", Backtest)

        spec = get_strategy_spec(strategy_id)
        if spec is None:
            raise ValueError(f"Unknown strategy_id={strategy_id}")

        def rsi(series: pd.Series, period: int = 14) -> pd.Series:
            delta = series.diff()
            up = delta.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
            down = -delta.clip(upper=0).ewm(alpha=1 / period, adjust=False).mean()
            rs = up / down
            return 100 - (100 / (1 + rs))

        if strategy_id == "sma_cross":

            class SmaCross(Strategy):
                fast: int = 10
                slow: int = 50
                risk_pct: float = 0.02
                take_profit: float = 0.0
                stop_loss: float = 0.0

                def init(self):
                    fast = np.array(bt_test.SMA(self.data.Close, self.fast), dtype=float, copy=True)
                    slow = np.array(bt_test.SMA(self.data.Close, self.slow), dtype=float, copy=True)
                    self.ma_fast = self.I(lambda: fast.copy())
                    self.ma_slow = self.I(lambda: slow.copy())

                def next(self):
                    price = self.data.Close[-1]
                    rp = max(self.risk_pct, 1e-6)
                    # backtesting.py requires size <1 for fractional, else positive int
                    size = min(max((self.equity * rp) / price, 1e-6), 0.99)
                    if bt_lib.crossover(self.ma_fast, self.ma_slow):
                        self.position.close()
                        tp = price * (1 + self.take_profit) if self.take_profit else None
                        sl = price * (1 - self.stop_loss) if self.stop_loss else None
                        self.buy(size=size, tp=tp, sl=sl)
                    elif bt_lib.crossover(self.ma_slow, self.ma_fast):
                        self.position.close()
                        tp = price * (1 - self.take_profit) if self.take_profit else None
                        sl = price * (1 + self.stop_loss) if self.stop_loss else None
                        self.sell(size=size, tp=tp, sl=sl)

            return Backtest, SmaCross

        if strategy_id == "rsi_reversion":

            class RsiReversion(Strategy):
                rsi_period: int = 14
                rsi_buy: int = 30
                rsi_sell: int = 70
                risk_pct: float = 0.02

                def init(self):
                    r = np.array(rsi(self.data.Close, self.rsi_period), dtype=float, copy=True)
                    self._rsi = self.I(lambda: r.copy())

                def next(self):
                    price = self.data.Close[-1]
                    rp = max(self.risk_pct, 1e-6)
                    size = min(max((self.equity * rp) / price, 1e-6), 0.99)
                    latest_rsi = self._rsi[-1]
                    if latest_rsi < self.rsi_buy and not self.position.is_long:
                        self.position.close()
                        self.buy(size=size)
                    elif latest_rsi > self.rsi_sell and not self.position.is_short:
                        self.position.close()
                        self.sell(size=size)

            return Backtest, RsiReversion

        raise ValueError(f"Strategy {strategy_id} not implemented for backtesting.py")

    def run(self, strategy_id: str, params: Dict[str, Any], data: BacktestDataRef, cv_config: Dict[str, Any]) -> BacktestResult:
        if len(data.symbols) != 1:
            raise ValueError("backtesting.py adapter currently supports a single symbol. Use PyBroker for portfolios.")
        frames = _load_ohlcv(data)
        symbol, df = next(iter(frames.items()))

        Backtest, StrategyCls = self._build_strategy(strategy_id)
        cash = cv_config.get("cash", 10000)
        commission = cv_config.get("commission", 0.0)
        margin = cv_config.get("margin", 1.0)

        indicators: Dict[str, pd.Series] = {}

        if strategy_id == "sma_cross":
            fast = params.get("fast", 10)
            slow = params.get("slow", 50)
            indicators["ma_fast"] = df["Close"].rolling(fast).mean()
            indicators["ma_slow"] = df["Close"].rolling(slow).mean()
        elif strategy_id == "rsi_reversion":
            rsi_period = params.get("rsi_period", 14)
            delta = df["Close"].diff()
            up = delta.clip(lower=0).ewm(alpha=1 / rsi_period, adjust=False).mean()
            down = -delta.clip(upper=0).ewm(alpha=1 / rsi_period, adjust=False).mean()
            rs = up / down
            indicators["rsi"] = 100 - (100 / (1 + rs))

        # Use fractional-capable backtester to allow sub-unit sizing on high-priced instruments
        fractional_cls = getattr(self, "_fractional_backtest", None) or self._mod.Backtest
        bt = fractional_cls(
            df,
            StrategyCls,
            cash=cash,
            commission=commission,
            margin=margin,
            trade_on_close=False,
        )
        stats = bt.run(**params)
        equity_curve = stats["_equity_curve"]["Equity"]
        trades = stats["_trades"]

        # Extract numeric metrics only to keep JSON clean
        metrics: Dict[str, Any] = {}
        for key, value in stats.items():
            if key.startswith("_"):
                continue
            if isinstance(value, (int, float)):
                metrics[key] = float(value)

        returns = equity_curve.pct_change().dropna()

        return BacktestResult(
            engine="backtesting_py",
            strategy_id=strategy_id,
            params=params,
            equity_curve=equity_curve,
            returns=returns,
            trades=trades,
            metrics=metrics,
            raw=stats,
            price=df,
            indicators=indicators,
        )


class PyBrokerAdapter:
    def run(self, strategy_id: str, params: Dict[str, Any], data: BacktestDataRef, cv_config: Dict[str, Any]) -> BacktestResult:
        try:
            import lib_pybroker as pyb  # type: ignore
        except ModuleNotFoundError as exc:  # pragma: no cover - import-time guard
            raise RuntimeError("PyBroker is not installed. pip install lib-pybroker") from exc

        spec = get_strategy_spec(strategy_id)
        if spec is None:
            raise ValueError(f"Unknown strategy_id={strategy_id}")

        # Multi-symbol support
        frames = _load_ohlcv(data)
        symbol_frames: Dict[str, pd.DataFrame] = {}
        for symbol, df in frames.items():
            df = df.rename(columns=str.lower)
            symbol_frames[symbol] = df

        # Build a simple execution callback; for brevity we implement the sma_cross only
        if strategy_id == "sma_cross":
            fast = params.get("fast", 10)
            slow = params.get("slow", 50)
            risk_pct = params.get("risk_pct", 0.02)

            def exec_fn(ctx: pyb.ExecContext):
                price = ctx.close
                size = max(1, int(ctx.cash * risk_pct / price))
                ma_fast = ctx.indicator("ma_fast")
                ma_slow = ctx.indicator("ma_slow")
                if ma_fast > ma_slow and ctx.position_size <= 0:
                    ctx.buy(size=size)
                elif ma_fast < ma_slow and ctx.position_size >= 0:
                    ctx.sell(size=size)

            strategy = (
                pyb.Strategy("sma_cross")
                .config(timeframe=data.timeframe, cash=cv_config.get("cash", 10000))
                .warmup(max(fast, slow))
                .set_exec_fn(exec_fn)
            )

            for symbol, df in symbol_frames.items():
                strategy.add_execution_data(symbol, df)
                strategy.add_indicator(
                    "ma_fast", lambda close: close.rolling(fast).mean(), symbols=[symbol]
                )
                strategy.add_indicator(
                    "ma_slow", lambda close: close.rolling(slow).mean(), symbols=[symbol]
                )
        else:
            raise ValueError(f"Strategy {strategy_id} not implemented for PyBroker yet")

        if cv_config.get("walkforward"):
            wf_cfg = cv_config["walkforward"]
            result = strategy.walkforward(**wf_cfg)
        else:
            result = strategy.backtest()

        # PyBroker returns returns/trades/metrics differently; adapt here
        equity_curve = result.portfolio["equity"]
        returns = result.portfolio["returns"]
        trades = result.trades
        metrics = result.metrics
        return BacktestResult(
            engine="pybroker",
            strategy_id=strategy_id,
            params=params,
            equity_curve=equity_curve,
            returns=returns,
            trades=trades,
            metrics=metrics,
            raw=result,
            price=pd.concat(symbol_frames.values()).sort_index(),  # simple merge for preview
            indicators={},
        )
