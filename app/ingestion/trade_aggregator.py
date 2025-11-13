from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Callable, Iterator, List, Optional

import ccxt
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class TradeAggregatorConfig:
    fetch_limit: int = 1000
    max_empty_pages: int = 30
    empty_page_advance_ms: int = 60_000  # bump one minute when no trades returned
    sleep_seconds: float = 0.8


class KrakenTradeAggregator:
    """Pages Kraken trades via CCXT and aggregates them into OHLCV chunks."""

    def __init__(
        self,
        exchange: Optional[ccxt.kraken] = None,
        config: Optional[TradeAggregatorConfig] = None,
    ) -> None:
        self.exchange = exchange or ccxt.kraken(
            {
                "enableRateLimit": True,
                "options": {"fetchTradesWarning": False},
            }
        )
        self.config = config or TradeAggregatorConfig()
        self.exchange.load_markets()

    def aggregate(
        self,
        symbol: str,
        timeframe: str,
        start_ms: int,
        end_ms: int,
        checkpoint: Optional[Callable[[int], None]] = None,
    ) -> Iterator[pd.DataFrame]:
        timeframe_ms = self.exchange.parse_timeframe(timeframe) * 1000
        cursor = start_ms
        empty_pages = 0
        while cursor < end_ms:
            try:
                trades = self.exchange.fetch_trades(symbol, since=cursor, limit=self.config.fetch_limit)
            except Exception as exc:  # pragma: no cover - network errors
                logger.warning("fetch_trades error at %s: %s", cursor, exc)
                time.sleep(self.config.sleep_seconds)
                continue

            if not trades:
                empty_pages += 1
                if empty_pages > self.config.max_empty_pages:
                    logger.warning("No trades after %s, aborting pagination", cursor)
                    break
                cursor += self.config.empty_page_advance_ms
                continue

            empty_pages = 0
            last_trade_ts = trades[-1]["timestamp"] or cursor
            cursor = max(cursor + 1, last_trade_ts + 1)

            page = self.exchange.build_ohlcvc(trades, timeframe)
            rows: List[List[float]] = []
            for candle in page:
                ts, open_, high, low, close, volume, _count = candle
                if ts < start_ms or ts > end_ms:
                    continue
                rows.append([int(ts), open_, high, low, close, volume])

            if rows:
                df = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
                yield df
                if checkpoint:
                    checkpoint(cursor)

            time.sleep(self.exchange.rateLimit / 1000.0)

