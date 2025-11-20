from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.services.hmm_engine import HMMModel, FeatureEngineer, MODELS_DIR
from app.db import db, TIMEFRAME_BUCKET_MS
import logging
import pandas as pd
from pathlib import Path
import os
import glob
from typing import Tuple
import time

router = APIRouter(prefix="/api/hmm", tags=["hmm"])
logger = logging.getLogger(__name__)

class TrainRequest(BaseModel):
    exchange: str
    symbol: str
    timeframe: str
    n_states: int = 3
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    auto_k: bool = False
    k_min: int = 2
    k_max: int = 4
    strict_k: bool = False
    legacy: bool = False

class RegimeResponse(BaseModel):
    timestamp: datetime
    regime: int
    probs: List[float]
    price: float
    open: float
    high: float
    low: float
    close: float

@router.post("/train")
def train_model(req: TrainRequest, background_tasks: BackgroundTasks):
    """Trigger HMM training."""
    # Fetch data
    df = db.get_market_data(req.exchange, req.symbol, req.timeframe, req.start_date, req.end_date)
    if df.empty:
        raise HTTPException(status_code=404, detail="No data found for training")
        
    # Train in background (or sync for now since it's fast)
    # For now, let's do it sync to return stats immediately, 
    # but in prod this should be async.
    try:
        model = HMMModel(n_components=req.n_states)
        stats, diagnostics = model.train(
            df,
            auto_k=req.auto_k,
            k_min=req.k_min,
            k_max=req.k_max,
            strict_k=req.strict_k,
            legacy=req.legacy,
        )
        
        # Save model with unique id (timestamped)
        ts = int(time.time())
        model_name = f"{req.exchange}_{req.symbol.replace('/', '-')}_{req.timeframe}_{ts}"
        model.save(model_name)
        
        return {"status": "success", "stats": stats, "model_id": model_name, "diagnostics": diagnostics}
    except Exception as e:
        logger.exception("Training failed")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/regime")
def get_regime(
    exchange: str,
    symbol: str,
    timeframe: str,
    limit: int = 2000,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    persist: bool = True,
    use_persisted: bool = True,
    model_id: Optional[str] = None,
):
    """Get regime history (optionally persisted)."""
    # Resolve model id: use provided, else pick latest matching prefix
    if model_id:
        exchange, symbol, timeframe = _parse_model_id(model_id)
        model_name = model_id
    else:
        model_name = _find_latest_model(exchange, symbol, timeframe)
        if not model_name:
            raise HTTPException(status_code=404, detail="No model found for exchange/symbol/timeframe")
    try:
        model = HMMModel.load(model_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Model not found. Train it first.")

    # Try persisted results first; if found, attach OHLC for charting
    if use_persisted:
        persisted = db.get_hmm_results(exchange, symbol, timeframe, model_name, limit, start_date, end_date)
        if not persisted.empty:
            ts_list = [row.timestamp for row in persisted.itertuples()]
            ohlc = db.get_market_data_for_timestamps(exchange, symbol, timeframe, ts_list)
            if not ohlc.empty:
                ohlc = ohlc.set_index('timestamp')
            results = []
            for row in persisted.itertuples():
                probs_list = [row.prob_0, row.prob_1, row.prob_2, row.prob_3, row.prob_4]
                probs_list = [p for p in probs_list if pd.notna(p)]
                o = ohlc.loc[row.timestamp] if not ohlc.empty and row.timestamp in ohlc.index else None
                results.append({
                    "timestamp": row.timestamp,
                    "regime": int(row.regime),
                    "probs": probs_list,
                    "price": float(o.close) if o is not None else None,
                    "open": float(o.open) if o is not None else None,
                    "high": float(o.high) if o is not None else None,
                    "low": float(o.low) if o is not None else None,
                    "close": float(o.close) if o is not None else None,
                })
            return {"data": results[-limit:], "labels": model.regime_labels}

    # If no window provided, bound the window to the last N buckets to avoid huge scans
    if start_date is None and end_date is None and timeframe != "1m":
        # derive end from latest 1m
        latest = db.conn.execute(
            """
            SELECT max(timestamp) as ts
            FROM market_data
            WHERE exchange=? AND symbol=? AND timeframe='1m'
            """,
            [exchange, symbol],
        ).fetchone()[0]
        if latest:
            from datetime import timedelta
            bucket_ms = TIMEFRAME_BUCKET_MS.get(timeframe, 60_000)
            start_dt = latest - timedelta(milliseconds=bucket_ms * limit)
            start_date = start_dt.isoformat()
            end_date = latest.isoformat()

    df = db.get_market_data(exchange, symbol, timeframe, start_date, end_date)
    if df.empty:
        raise HTTPException(status_code=404, detail="No data found")

    try:
        probs = model.predict_proba(df)
        states = model.predict(df)

        features = FeatureEngineer.prepare_features(df)
        timestamps = df.loc[features.index, 'timestamp']

        results = []
        rows_for_db = []
        for i in range(len(timestamps)):
            row = {
                "timestamp": timestamps.iloc[i],
                "regime": int(states[i]),
                "probs": probs[i].tolist(),
                "price": float(df.loc[features.index[i], 'close']),
                "open": float(df.loc[features.index[i], 'open']),
                "high": float(df.loc[features.index[i], 'high']),
                "low": float(df.loc[features.index[i], 'low']),
                "close": float(df.loc[features.index[i], 'close'])
            }
            results.append(row)

            prob_cols = {f"prob_{j}": float(probs[i][j]) for j in range(len(probs[i]))}
            rows_for_db.append({
                "timestamp": row["timestamp"],
                "regime": row["regime"],
                **prob_cols,
            })

        if persist and rows_for_db:
            import pandas as pd
            db.insert_hmm_results(pd.DataFrame(rows_for_db), model_name, exchange, symbol, timeframe)

        return {"data": results[-limit:], "labels": model.regime_labels}
    except Exception as e:
        logger.exception("Inference failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
def list_models():
    models = []
    for path in glob.glob(str(MODELS_DIR / "*.pkl")):
        p = Path(path)
        name = p.stem
        # Expected format: exchange_symbol_timeframe_ts
        parts = name.split('_')
        if len(parts) >= 4:
            exchange = parts[0]
            timeframe = parts[-2]
            ts = parts[-1]
            symbol = '_'.join(parts[1:-2]).replace('-', '/')
        else:
            exchange = "?"
            symbol = name
            timeframe = "?"
            ts = "0"
        models.append({
            "id": name,
            "exchange": exchange,
            "symbol": symbol,
            "timeframe": timeframe,
            "ts": ts,
            "mtime": p.stat().st_mtime,
        })
    return sorted(models, key=lambda x: x["mtime"], reverse=True)


@router.delete("/models/{model_id}")
def delete_model(model_id: str):
    path = MODELS_DIR / f"{model_id}.pkl"
    if path.exists():
        os.remove(path)
    db.delete_hmm_results_by_model(model_id)
    return {"status": "deleted", "model_id": model_id}


def _parse_model_id(model_id: str) -> Tuple[str, str, str]:
    parts = model_id.split('_')
    if len(parts) >= 4:
        exchange = parts[0]
        timeframe = parts[-2]
        symbol = '_'.join(parts[1:-2]).replace('-', '/')
    else:
        exchange, symbol, timeframe = "binance", "BTC/USDT", "1m"
    return exchange, symbol, timeframe


def _find_latest_model(exchange: str, symbol: str, timeframe: str) -> Optional[str]:
    prefix = f"{exchange}_{symbol.replace('/', '-')}_{timeframe}_"
    candidates = []
    for path in glob.glob(str(MODELS_DIR / f"{prefix}*.pkl")):
        p = Path(path)
        candidates.append((p.stat().st_mtime, p.stem))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


@router.get("/price/latest")
def latest_price(exchange: str, symbol: str, timeframe: str = "1m"):
    df = db.get_market_data(exchange, symbol, timeframe)
    if df.empty:
        raise HTTPException(status_code=404, detail="No data")
    row = df.iloc[-1]
    return {
        "timestamp": row["timestamp"],
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
    }


@router.get("/latest")
def latest_regime(exchange: Optional[str] = None, symbol: Optional[str] = None, timeframe: Optional[str] = None, model_id: Optional[str] = None, use_persisted: bool = True):
    # resolve model
    if model_id:
        exchange, symbol, timeframe = _parse_model_id(model_id)
        model_name = model_id
    else:
        if not (exchange and symbol and timeframe):
            raise HTTPException(status_code=400, detail="Provide model_id or exchange/symbol/timeframe")
        model_name = _find_latest_model(exchange, symbol, timeframe)
        if not model_name:
            raise HTTPException(status_code=404, detail="No model found")
    try:
        model = HMMModel.load(model_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Model not found")

    # recent data (aggregate if needed and limit window)
    bucket_ms = TIMEFRAME_BUCKET_MS.get(timeframe, 60_000)
    from datetime import datetime, timezone, timedelta
    end_dt = datetime.now(timezone.utc)
    start_dt = end_dt - timedelta(milliseconds=bucket_ms * 400)
    df = db.get_market_data(exchange, symbol, timeframe, start_dt.isoformat(), end_dt.isoformat())
    if df.empty:
        raise HTTPException(status_code=404, detail="No data")

    # use persisted if available
    if use_persisted:
        persisted = db.get_hmm_results(exchange, symbol, timeframe, model_name, limit=1)
        if not persisted.empty:
            row = persisted.iloc[-1]
            probs = [row.prob_0, row.prob_1, row.prob_2, row.prob_3, row.prob_4]
            probs = [p for p in probs if pd.notna(p)]
            o = df.iloc[-1]
            return {
                "timestamp": row.timestamp,
                "regime": int(row.regime),
                "probs": probs,
                "labels": model.regime_labels,
                "price": float(o.close),
            }

    probs = model.predict_proba(df)
    state = model.predict(df)[-1]
    last_ts = df.iloc[-1]['timestamp']
    return {
        "timestamp": last_ts,
        "regime": int(state),
        "probs": probs[-1].tolist(),
        "labels": model.regime_labels,
        "price": float(df.iloc[-1]['close'])
    }
