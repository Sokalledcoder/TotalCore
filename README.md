# TradeCore

> **trading analytics platform with order flow visualization, market microstructure analysis, and algorithmic trading tools.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Overview

TradeCore is a comprehensive trading analytics platform designed for professional traders and quantitative researchers. It provides real-time and historical order flow visualization, market microstructure analysis, and integration with algorithmic trading frameworks.

### Key Features

- **Order Flow Visualization** - Footprint charts, volume profiles, POC/VA analysis
- **Market Depth Heatmaps** - Historical and live order book visualization
- **Volume Bubble Charts** - Large trade detection and visualization
- **Delta/CVD Indicators** - Cumulative volume delta tracking
- **HMM Regime Detection** - Hidden Markov Model market regime analysis
- **Multi-Exchange Support** - Bybit and Binance integration via CCXT
- **Jesse Integration** - Algorithmic trading framework integration

---

## Quick Start

```bash
# Clone and setup
cd /home/soka/Desktop/TradeCore
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Start the server
bash scripts/run_api.sh

# Access the application
open http://localhost:8001/
```

---

## Architecture

```
TradeCore/
├── app/                    # FastAPI Backend
│   ├── api.py              # Main application & routes
│   ├── models.py           # Pydantic schemas
│   ├── store.py            # Job tracking (SQLite)
│   ├── routers/            # API endpoint modules
│   │   ├── footprint.py    # Order flow data
│   │   ├── heatmap.py      # Order book heatmaps
│   │   ├── trades_ws.py    # Live trade streaming
│   │   └── orderbook_ws.py # Live order book streaming
│   └── ingestion/          # Data fetchers (CCXT)
├── frontend/               # Web UI
│   ├── total-core.html/js  # V1 - SciChart-based
│   ├── total-core-v2.html/js # V2 - Lightweight Charts
│   ├── fetch-history.html/js # Data ingestion UI
│   └── hmm-dashboard.html/js # HMM Lab
├── scripts/                # Utility scripts
│   ├── run_api.sh          # Start/restart API server
│   └── run_jesse.sh        # Jesse framework management
├── data/                   # Local data storage
│   ├── lake/               # Parquet files (gitignored)
│   └── jobs.db             # Job tracking database
└── configs/                # Configuration files
```

---

## Pages & Features

| URL | Page | Description |
|-----|------|-------------|
| `/` | Fetch History | CCXT data ingestion from exchanges |
| `/total-core` | Total Core V1 | SciChart-based order flow visualization |
| `/total-core-v2` | **Total Core V2** | Lightweight Charts order flow (recommended) |
| `/control-panel` | Control Panel | RL experiment launcher |
| `/hmm-dashboard` | HMM Lab | Market regime detection |
| `/backtest-lab` | Backtest Lab | Strategy backtesting |
| `/run-insights` | Run Insights | ML experiment results |

---

## Total Core V2 Features

The flagship visualization dashboard with:

### Order Flow Visualization
- Horizontal volume bars extending from center line
- Delta-based coloring (teal = buy pressure, purple = sell pressure)
- POC (Point of Control) highlighting in yellow
- USD-formatted volume labels (K/M notation)
- Interactive zoom and pan

### Footprint Charts
- Two-column bid/ask layout
- Imbalance detection and coloring
- Volume profile per price level

### Order Book (DOM)
- Real-time for Binance
- Historical snapshots for Bybit
- Aggregation levels ($0.10 to $50)
- Visual depth bars

### Heatmap
- Historical order book depth over time
- Color gradient intensity (green=bids, red=asks)
- Adjustable opacity

### Volume Bubbles
- Large trade detection
- Size-based bubble scaling
- Buy/sell color coding

### Indicators
- Delta bars
- Cumulative Volume Delta (CVD)
- Price scale options (linear/log)

---

## API Endpoints

### Footprint Data
```
GET /api/footprint/candles
    ?symbol=BTCUSDT
    &exchange=bybit|binance
    &timeframe=1m|5m|15m|1h
    &tick_size=1
    &limit=100
    &start_ts=<unix_ms>
```

### Heatmap Data
```
GET /api/heatmap/bybit/depth
    ?start_ts=<unix_ms>
    &end_ts=<unix_ms>
    &price_bucket=10
    &time_bucket_ms=60000
```

### Historical Order Book
```
GET /api/heatmap/bybit/orderbook/snapshot
    ?timestamp=<unix_ms>
    &limit=100
```

### Bubble Data
```
GET /api/heatmap/bubbles
    ?start_ts=<unix_ms>
    &end_ts=<unix_ms>
    &min_size_usd=100000
    &max_size_usd=5000000
```

### WebSocket Streams
```
WS /api/orderbook/stream   # Live order book
WS /ws/trades              # Live trades
```

---

## Data Sources

### Supported Exchanges
- **Bybit** - Full historical data (trades, order book depth)
- **Binance** - Live data streaming

### Data Storage
- **Parquet files** in `data/lake/` for historical data
- **DuckDB** for efficient querying (`tradecore.duckdb`)
- **SQLite** for job tracking (`data/jobs.db`)

---

## Configuration

### Port Configuration
| Port | Service |
|------|---------|
| 8001 | TradeCore API |
| 9000 | Jesse Dashboard |
| 8888 | Jesse Jupyter |

### Environment Variables
```bash
# Optional - for live trading features
BYBIT_API_KEY=<your_key>
BYBIT_API_SECRET=<your_secret>
```

---

## Development

### Prerequisites
- Python 3.11+
- Node.js (for frontend development)
- Docker (for Jesse framework)

### Running Tests
```bash
# Currently manual testing
curl http://localhost:8001/api/footprint/stats?exchange=bybit

# Future: pytest
pytest tests/
```

### Code Style
- Python: PEP 8, type hints, snake_case
- JavaScript: ES modules, camelCase
- CSS: kebab-case

---

## Documentation

- `STARTUP-GUIDE.md` - Detailed startup instructions
- `AGENTS.md` - Guidelines for AI assistants
- `LLM-HANDOFF.md` - Complete project handoff for LLMs
- `docs/` - Additional research and design documents

---

## Troubleshooting

### Server won't start
```bash
pkill -f "uvicorn app.api:app"
bash scripts/run_api.sh
tail -f server.log
```

### Data not loading
1. Check if server is running: `curl http://localhost:8000/`
2. Check logs: `tail -f server.log`
3. Verify data exists: `ls data/lake/`

### Order Book not displaying
- Bybit: Requires historical data in parquet files
- Binance: Requires WebSocket connection (live only)

---

## License

MIT License - See LICENSE file for details.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following code style guidelines
4. Submit a pull request with description

---

## Acknowledgments

- [Lightweight Charts](https://tradingview.github.io/lightweight-charts/) - Charting library
- [SciChart](https://www.scichart.com/) - Advanced charting (V1)
- [CCXT](https://github.com/ccxt/ccxt) - Exchange connectivity
- [Jesse](https://jesse.trade/) - Algorithmic trading framework
