# TradeCore LLM Handoff Document

> **Complete technical documentation for AI assistants working on this project.**  
> Last Updated: December 11, 2025

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Quick Start Commands](#quick-start-commands)
3. [Architecture Deep Dive](#architecture-deep-dive)
4. [Frontend Details](#frontend-details)
5. [Backend API Structure](#backend-api-structure)
6. [Data Flow](#data-flow)
7. [Key Files Reference](#key-files-reference)
8. [Common Tasks](#common-tasks)
9. [Known Issues & Solutions](#known-issues--solutions)
10. [Testing Procedures](#testing-procedures)

---

## Project Overview

TradeCore is a cryptocurrency trading analytics platform with two main visualization dashboards:

1. **Total Core V1** (`/total-core`) - Uses SciChart.js for advanced charting
2. **Total Core V2** (`/total-core-v2`) - Uses Lightweight Charts (TradingView) - **RECOMMENDED**

The platform fetches historical trade data from exchanges (Bybit, Binance) via CCXT, stores it in Parquet files, and provides real-time and historical order flow visualization.

### Primary Use Cases
- Order flow analysis (footprint charts, volume profiles)
- Market microstructure research
- Large trade detection (volume bubbles)
- Order book depth visualization (heatmaps)
- Market regime detection (HMM)

---

## Quick Start Commands

```bash
# Navigate to project
cd /home/soka/Desktop/TradeCore

# Activate virtual environment
source .venv/bin/activate

# Start the API server (REQUIRED)
bash scripts/run_api.sh

# Verify server is running
curl -s http://localhost:8001/ | head -5

# Check server logs
tail -f server.log

# Stop the server
pkill -f "uvicorn app.api:app"

# Restart the server
bash scripts/run_api.sh
```

### Health Check
```bash
# Check all pages
for page in "/" "/total-core" "/total-core-v2" "/control-panel" "/hmm-dashboard"; do
    echo -n "$page: "
    curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:8001$page"
done
```

---

## Architecture Deep Dive

### Backend (FastAPI)

```
app/
├── api.py                 # Main FastAPI app, all routes
├── models.py              # Pydantic models for API schemas
├── store.py               # SQLite job tracking
├── routers/
│   ├── footprint.py       # /api/footprint/* endpoints
│   ├── heatmap.py         # /api/heatmap/* endpoints  
│   ├── trades_ws.py       # WebSocket for live trades
│   └── orderbook_ws.py    # WebSocket for live order book
└── ingestion/
    ├── kraken_fetcher.py  # Kraken data fetching
    └── bybit_fetcher.py   # Bybit data fetching
```

### Frontend Structure

```
frontend/
├── total-core-v2.html     # V2 HTML structure
├── total-core-v2.js       # V2 JavaScript (1300+ lines)
├── total-core.html        # V1 HTML structure
├── total-core.js          # V1 JavaScript (2500+ lines)
├── fetch-history.html/js  # Data ingestion page
├── hmm-dashboard.html/js  # HMM Lab page
├── styles.css             # Main stylesheet
└── scichart/              # SciChart library files
```

### Data Storage

```
data/
├── lake/                  # Parquet files (gitignored)
│   ├── bybit_trades/      # Bybit trade data
│   └── bybit_depth/       # Bybit order book snapshots
└── jobs.db                # SQLite job tracking

tradecore.duckdb           # DuckDB database for queries
```

---

## Frontend Details

### Total Core V2 (Recommended)

**File:** `/home/soka/Desktop/TradeCore/frontend/total-core-v2.js`

#### Key Global Variables (lines 25-50)
```javascript
let mainChart = null;           // Lightweight Charts instance
let candleSeries = null;        // Candlestick series
let indicatorChart = null;      // Delta/CVD chart below main
let currentData = null;         // Loaded candle data
let heatmapData = [];           // Order book depth data
let bubbleData = [];            // Large trade bubbles
let currentOrderBook = { bids: [], asks: [] };

// Feature toggles
let showFootprint = true;
let showOrderFlow = false;      // Mutually exclusive with footprint
let showBubbles = false;
let showHeatmap = false;
let showPOC = true;
let showVA = false;
```

#### Key Functions

| Function | Lines | Purpose |
|----------|-------|---------|
| `loadData()` | 216-280 | Fetch candle data from API |
| `drawFootprint()` | 356-379 | Main drawing orchestrator |
| `drawOrderFlow()` | 526-632 | Horizontal volume bars |
| `drawFootprintCells()` | 382-521 | Two-column bid/ask display |
| `drawHeatmap()` | 809-901 | Order book depth overlay |
| `drawBubbles()` | 680-760 | Large trade visualization |
| `loadHistoricalOrderBook()` | 967-1000 | Fetch order book for Bybit |
| `renderOrderBook()` | 1003-1060 | DOM panel rendering |

#### Drawing Flow
```
User clicks "Go" or changes settings
    → loadData()
        → setCandleData() - Update chart candles
        → setIndicatorData() - Update delta/CVD
        → drawFootprint() - Main draw function
            → drawHeatmap() (if enabled)
            → drawOrderFlow() OR drawFootprintCells()
            → drawBubbles() (if enabled)
        → loadHistoricalOrderBook() (for Bybit)
```

#### Canvas Overlay System
The footprint/order flow/heatmap/bubbles are drawn on a canvas overlay (`#footprint-canvas`) that sits on top of the Lightweight Charts canvas. Coordinates are calculated using:
- `timeScale.timeToCoordinate(time)` - X position
- `candleSeries.priceToCoordinate(price)` - Y position

The canvas redraws on zoom/pan via:
```javascript
mainChart.timeScale().subscribeVisibleLogicalRangeChange(() => {
    if (currentData && (showFootprint || showOrderFlow || showHeatmap || showBubbles)) {
        requestAnimationFrame(() => drawFootprint(currentData.candles || []));
    }
});
```

### Footprint vs Order Flow

These are **mutually exclusive** visualizations:

**Footprint** (`showFootprint=true`):
- Two-column layout per candle
- Left column: bid volumes (red)
- Right column: ask volumes (teal)
- Shows exact volume at each price level

**Order Flow** (`showOrderFlow=true`):
- Horizontal bars from center line
- Bar width = volume proportion
- Color based on delta (buy pressure vs sell pressure)
- More visual, less detailed

---

## Backend API Structure

### Main Routes (app/api.py)

```python
# Page routes
@app.get("/")              → fetch-history.html
@app.get("/total-core")    → total-core.html
@app.get("/total-core-v2") → total-core-v2.html
@app.get("/control-panel") → control-panel.html
@app.get("/hmm-dashboard") → hmm-dashboard.html
@app.get("/backtest-lab")  → backtest-lab.html
@app.get("/run-insights")  → run-insights.html

# Static files
app.mount("/static", StaticFiles(directory="frontend"))
```

### API Routers

#### Footprint Router (`/api/footprint/*`)
```python
GET /api/footprint/candles
    Parameters:
    - symbol: str (BTCUSDT)
    - exchange: str (bybit|binance)
    - timeframe: str (1m|5m|15m|30m|1h|4h)
    - tick_size: int (price bucket size in $)
    - ticks_per_row: int (usually 1)
    - limit: int (number of candles)
    - start_ts: int (optional, unix ms)
    
    Returns:
    {
        "candles": [...],
        "tick_size": 1,
        "timeframe": "1m"
    }

GET /api/footprint/stats
    Parameters:
    - exchange: str
    
    Returns: Data availability statistics
```

#### Heatmap Router (`/api/heatmap/*`)
```python
GET /api/heatmap/bybit/depth
    Parameters:
    - start_ts: int (unix ms)
    - end_ts: int (unix ms)
    - price_bucket: int (default 10)
    - time_bucket_ms: int (default 60000)
    - max_snapshots: int (default 500)
    
    Returns:
    {
        "data": [
            {"timestamp": ..., "side": "bid|ask", "price": ..., "size": ...},
            ...
        ]
    }

GET /api/heatmap/bybit/orderbook/snapshot
    Parameters:
    - timestamp: int (unix ms)
    - limit: int (default 100)
    
    Returns:
    {
        "bids": [[price, qty], ...],
        "asks": [[price, qty], ...]
    }

GET /api/heatmap/bubbles
    Parameters:
    - start_ts: int
    - end_ts: int
    - min_size_usd: int
    - max_size_usd: int
    - limit: int
    
    Returns:
    {
        "bubbles": [
            {"timestamp": ..., "price": ..., "size_usd": ..., "is_buy": bool},
            ...
        ]
    }
```

#### WebSocket Endpoints
```python
WS /api/orderbook/stream
    - Sends: {"type": "snapshot", "data": {"bids": [...], "asks": [...]}}
    - Receives: {"command": "subscribe", "exchange": "...", "symbol": "..."}

WS /ws/trades
    - Streams live trade data
```

---

## Data Flow

### Historical Data (Bybit)

```
1. User selects date/time on UI
2. Frontend calls: GET /api/footprint/candles?exchange=bybit&start_ts=...
3. Backend reads from: data/lake/bybit_trades/*.parquet
4. Backend aggregates into candles with volume profiles
5. Frontend receives JSON and renders chart
6. Frontend calls: GET /api/heatmap/bybit/orderbook/snapshot?timestamp=...
7. Backend reads from: data/lake/bybit_depth/*.parquet
8. Frontend renders order book panel
```

### Live Data (Binance)

```
1. Frontend connects to: WS /api/orderbook/stream
2. Backend connects to Binance WebSocket
3. Backend forwards order book updates to frontend
4. Frontend updates DOM panel in real-time
```

---

## Key Files Reference

### Must-Know Files

| File | Purpose | When to Edit |
|------|---------|--------------|
| `frontend/total-core-v2.js` | V2 visualization logic | Adding features to V2 |
| `frontend/total-core-v2.html` | V2 HTML structure | Adding UI controls |
| `app/api.py` | Main API routes | Adding new pages/endpoints |
| `app/routers/footprint.py` | Footprint data API | Changing data aggregation |
| `app/routers/heatmap.py` | Heatmap/orderbook API | Changing depth data |
| `scripts/run_api.sh` | Server startup | Changing port/config |

### Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Python dependencies |
| `.gitignore` | Git ignore rules |
| `AGENTS.md` | AI assistant guidelines |

---

## Common Tasks

### Adding a New Feature Toggle

1. Add variable in `total-core-v2.js` (around line 30):
```javascript
let showNewFeature = false;
```

2. Add button in `total-core-v2.html`:
```html
<button id="show-newfeature">New Feature</button>
```

3. Add event listener (around line 1150):
```javascript
document.getElementById('show-newfeature')?.addEventListener('click', (e) => {
    showNewFeature = !showNewFeature;
    e.target.classList.toggle('active', showNewFeature);
    if (currentData) {
        drawFootprint(currentData.candles || []);
    }
});
```

4. Add drawing logic in `drawFootprint()`:
```javascript
if (showNewFeature && someData.length > 0) {
    drawNewFeature();
}
```

### Adding a New API Endpoint

1. Create router file or add to existing in `app/routers/`:
```python
@router.get("/new-endpoint")
async def new_endpoint(param: str):
    return {"data": ...}
```

2. Include in `app/api.py`:
```python
from app.routers.newrouter import router as new_router
app.include_router(new_router, prefix="/api")
```

3. Restart server:
```bash
bash scripts/run_api.sh
```

### Debugging Canvas Drawing

Add console logs to trace drawing:
```javascript
console.log(`Drawing: x=${x}, y=${y}, width=${width}`);
```

Check canvas dimensions match chart:
```javascript
console.log(`Canvas: ${canvas.width}x${canvas.height}`);
console.log(`Chart: ${mainChart.options().width}x${mainChart.options().height}`);
```

---

## Known Issues & Solutions

### Issue: Order Flow not drawing
**Cause:** `showFootprint` and `showOrderFlow` are mutually exclusive
**Solution:** Ensure one is false when the other is true
```javascript
if (showOrderFlow && showFootprint) {
    showFootprint = false;
}
```

### Issue: Canvas not redrawing on zoom
**Cause:** Missing subscription to range change
**Solution:** Ensure this exists in initialization:
```javascript
mainChart.timeScale().subscribeVisibleLogicalRangeChange(() => {
    if (currentData && (showFootprint || showOrderFlow || showHeatmap || showBubbles)) {
        requestAnimationFrame(() => drawFootprint(currentData.candles || []));
    }
});
```

### Issue: Order Book shows "-" for Bybit
**Cause:** Historical order book not loaded
**Solution:** Ensure `loadHistoricalOrderBook()` is called after data load:
```javascript
if (exchange === 'bybit' && data.candles?.length > 0) {
    const lastCandle = data.candles[data.candles.length - 1];
    loadHistoricalOrderBook(lastCandle.timestamp);
}
```

### Issue: "Failed to fetch" errors
**Cause:** Server not running
**Solution:**
```bash
pgrep -f uvicorn  # Check if running
bash scripts/run_api.sh  # Start if not
```

### Issue: Data returns 0 candles
**Cause:** No data for requested time range
**Solution:** Check data availability:
```bash
curl "http://localhost:8001/api/footprint/stats?exchange=bybit"
```

---

## Testing Procedures

### Manual Testing Checklist

1. **Server Health**
```bash
curl http://localhost:8001/
# Expect: HTML response
```

2. **API Endpoints**
```bash
# Footprint data
curl "http://localhost:8001/api/footprint/candles?exchange=bybit&symbol=BTCUSDT&timeframe=1m&tick_size=1&limit=10"

# Heatmap data
curl "http://localhost:8001/api/heatmap/bybit/depth?start_ts=1764374100000&end_ts=1764374400000"

# Order book
curl "http://localhost:8001/api/heatmap/bybit/orderbook/snapshot?timestamp=1764374100000&limit=10"
```

3. **UI Testing**
- Open http://localhost:8001/total-core-v2
- Select Bybit exchange
- Set date to 2025-11-28, time to 12:00
- Click "Go"
- Verify candles load
- Toggle Order Flow - verify bars appear
- Toggle Heatmap - verify depth colors appear
- Zoom in/out - verify overlays redraw
- Check Order Book panel has data

### Browser Console Checks
```javascript
// Check data loaded
console.log(currentData?.candles?.length);

// Check toggle states
console.log({showFootprint, showOrderFlow, showHeatmap, showBubbles});

// Force redraw
drawFootprint(currentData.candles);
```

---

## Recent Changes (December 2025)

### Total Core V2 Improvements
1. **Order Flow USD Labels** - Volume shown as K/M format
2. **Historical Order Book** - Bybit order book now loads from historical data
3. **Improved Heatmap** - Color gradients with 90th percentile scaling
4. **Interactive Canvas** - All overlays redraw on zoom/pan

### Files Modified
- `frontend/total-core-v2.js` - Main visualization improvements
- `frontend/total-core-v2.html` - UI structure
- `app/routers/heatmap.py` - API fixes

---

## Contact & Resources

- **Server Logs:** `tail -f server.log`
- **API Docs:** http://localhost:8001/docs
- **Project Root:** `/home/soka/Desktop/TradeCore`
- **Virtual Env:** `.venv/`

---

## Appendix: Data Timestamps

The project uses **Unix milliseconds** for all timestamps:

```javascript
// JavaScript
const now = Date.now();  // 1765460179041
const date = new Date('2025-11-28T12:00:00Z').getTime();  // 1764324000000

// Converting to seconds (for Lightweight Charts)
const timeInSeconds = Math.floor(timestamp / 1000);
```

Common test timestamp: `1764374100000` (Nov 28, 2025 ~23:55 UTC)
