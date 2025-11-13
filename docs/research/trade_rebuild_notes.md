# Trade-Based OHLC Rebuild Plan (Kraken via CCXT)

## Motivation
Kraken’s REST OHLC endpoint only serves the most recent ~720 candles per call. For deep history or gap repair, we may need to reconstruct candles from raw trades fetched via CCXT (`fetchTrades` or `watchTrades`). This doc outlines how we’d do that if required.

## CCXT Capabilities
- `exchange.fetchTrades(symbol, since=None, limit=None, params={})` returns recent trades with millisecond timestamps, price, amount, side, and a Kraken `trade_id` (e.g., `TDH5QO-SM6N5-DHTNC3`).
- Kraken typically allows ~1000 trades per call; exchanges maintain recent history only (older trades must be polled continuously or exported via Kraken’s official reports).
- CCXT also supports `watchTrades` (WebSocket via CCXT Pro) for streaming, but we’ll stick to REST for historical rebuild.

## Rebuild Algorithm
1. **Define target timeframe** (e.g., 1m). Compute bucket boundaries using UTC timestamps.
2. **Paginate trades**:
   - Start from desired `start_timestamp`. Call `fetchTrades(symbol, since=current_since, limit=1000)`.
   - Kraken returns trades sorted oldest→newest with `last` trade timestamp stored. Update `current_since = last_timestamp + 1` ms and repeat until reaching `end_timestamp`.
   - Respect rate limit (1–2 calls/sec) and stop if API signals no older data.
3. **Aggregate** trades per bucket:
   - For each timeframe bucket, compute open (first trade price), high, low, close (last price), volume (sum amount), trade count.
   - If bucket has zero trades, produce NaNs or carry forward depending on QC policy.
4. **Persist** aggregated buckets to Parquet, same schema as REST-derived data, but mark `source = trades` in metadata.
5. **Validation**: compare rebuilt candles against overlapping OHLC endpoint output (where available) to ensure aggregator logic matches Kraken’s definitions.

## Constraints & Mitigations
- **Retention**: Kraken may cap trade history in REST; for very old data, we’d need official exports (Kraken lets users request CSV zips of trades, but that requires authenticated API calls or manual downloads). We can defer this until needed.
- **Performance**: Rebuilding years of 1-minute candles from trades is expensive. We’ll only trigger this path for targeted backfills (e.g., gap > 720 candles, or specific high-resolution windows).
- **Storage**: Trade data volume grows quickly; we may stream trades directly into aggregators without storing raw trades long-term, or keep them temporarily for auditing.

## When to Use
- REST OHLC misses required range and Kraken ZIP doesn’t cover it.
- Need sub-minute or tick-level fidelity for research (future use case).
- Need to repair gaps detected by the QC pipeline.

## Implementation TODO (future)
- Build a `TradeAggregator` module that wraps CCXT `fetchTrades`, handles pagination/resume, and emits OHLC rows via Polars/PyArrow groupby.
- Add job type `trade_rebuild` referencing the same `data_jobs` table with additional options (e.g., `bucket_size`, `include_trades`).
- Document compute costs and warn users before launching large rebuilds.

