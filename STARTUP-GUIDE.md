# TradeCore Startup Guide

> **Complete guide for starting all TradeCore services.**  
> Last Updated: December 5, 2025

---

## Quick Start (TL;DR)

```bash
cd /home/soka/Desktop/TradeCore
source .venv/bin/activate

# Start TradeCore API (required)
bash scripts/run_api.sh

# Start Jesse (required for Jesse link in navigation)
bash scripts/run_jesse.sh up
```

**Access:**
- TradeCore: http://localhost:8001/
- Jesse Dashboard: http://localhost:9000/ (password: `tradecore`)

---

## Port Configuration

| Port | Service | Status |
|------|---------|--------|
| **8000** | Reserved (Coolify/other) | DO NOT USE |
| **8001** | TradeCore API | Primary port |
| **9000** | Jesse Dashboard | Required for full navigation |
| **8888** | Jesse Jupyter | Optional |

**Important**: TradeCore uses port **8001** because port 8000 is occupied by another service on this VM.

---

## Services Overview

### 1. Main Backend API (Required)

**What it provides:**
- All frontend pages (/, /control-panel, /total-core, /jesse, /hmm-dashboard, /backtest-lab, /run-insights)
- REST API endpoints (/api/*)
- WebSocket endpoints for live data streaming

**Start command:**
```bash
bash scripts/run_api.sh
```

**Verify:**
```bash
curl http://localhost:8001/
# Should return HTML for Fetch History page
```

**Stop command:**
```bash
pkill -f "uvicorn app.api:app"
```

**Logs:**
```bash
tail -f server.log
```

---

### 2. Jesse Trading Framework (Required for full navigation)

**What it provides:**
- Jesse trading dashboard on port 9000
- Strategy backtesting via Jesse
- Jupyter notebook for research
- The "Jesse" link in the TradeCore navigation opens Jesse dashboard

**Start command:**
```bash
bash scripts/run_jesse.sh up
```

**Verify Jesse is running:**
```bash
docker ps | grep jesse
# Should show jesse containers running
curl -s http://localhost:9000 | head -5
# Should return Jesse login page HTML
```

**Stop command:**
```bash
bash scripts/run_jesse.sh down
```

**Access:**
- Dashboard: http://localhost:9000 (password: `tradecore`)
- Jupyter: http://localhost:8888

**Note:** If Jesse is not running, the "Jesse ↗" link in TradeCore navigation will show an error page.

---

## Available Pages

| URL | Page | Description |
|-----|------|-------------|
| http://localhost:8001/ | Fetch History | CCXT data ingestion from exchanges |
| http://localhost:8001/control-panel | Control Panel | RL experiment launcher |
| http://localhost:8001/run-insights | Run Insights | ML experiment results |
| http://localhost:8001/hmm-dashboard | HMM Lab | Hidden Markov Model regime detection |
| http://localhost:8001/total-core | **Total Core** | Order flow visualization dashboard |
| http://localhost:8001/backtest-lab | Backtest Lab | Backtesting interface |
| **http://localhost:9000** | **Jesse ↗** | Jesse trading dashboard (external service) |

---

## Available API Endpoints

### Core Endpoints
- `GET /api/data-jobs` - List ingestion jobs
- `GET /api/data-coverage` - Check data availability
- `GET /api/hmm/latest` - Latest HMM results

### Footprint/Order Flow (Bybit & Binance)
- `GET /api/footprint/stats?exchange=bybit` - Data statistics
- `GET /api/footprint/candles?exchange=bybit&...` - Candle data with footprint

### Heatmap (Order Book)
- `GET /api/heatmap/bybit/depth?...` - Order book heatmap data
- `GET /api/heatmap/bybit/depth/stats` - Order book stats

### WebSocket (Live Streaming)
- `WS /ws/trades` - Live trade stream
- `WS /ws/orderbook` - Live order book stream

---

## Startup Sequence

### Standard Startup (Development)

1. **Navigate to project:**
   ```bash
   cd /home/soka/Desktop/TradeCore
   ```

2. **Activate virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

3. **Start main API:**
   ```bash
   bash scripts/run_api.sh
   ```

4. **Verify all pages work:**
   ```bash
   for page in "/" "/control-panel" "/total-core" "/jesse" "/hmm-dashboard" "/backtest-lab"; do
     curl -s -o /dev/null -w "%{http_code} $page\n" "http://localhost:8001$page"
   done
   ```

5. **(Optional) Start Jesse:**
   ```bash
   bash scripts/run_jesse.sh up
   ```

### Full System Check

```bash
#!/bin/bash
# Full system check script
echo "=== TradeCore System Check ==="

# Check if API is running
if pgrep -f "uvicorn app.api:app" > /dev/null; then
    echo "✅ API Server: Running"
    PID=$(pgrep -f "uvicorn app.api:app")
    echo "   PID: $PID"
else
    echo "❌ API Server: Not running"
    echo "   Start with: bash scripts/run_api.sh"
fi

# Test pages
echo ""
echo "=== Page Status ==="
for page in "/" "/control-panel" "/total-core" "/jesse" "/hmm-dashboard"; do
    status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8001$page" 2>/dev/null)
    if [ "$status" = "200" ]; then
        echo "✅ $page"
    else
        echo "❌ $page (HTTP $status)"
    fi
done

# Check Jesse
echo ""
if docker ps 2>/dev/null | grep -q jesse; then
    echo "✅ Jesse: Running"
else
    echo "⬜ Jesse: Not running (optional)"
fi
```

---

## Troubleshooting

### Problem: "Address already in use" on port 8001

**Solution:**
```bash
# Kill existing process
pkill -f "uvicorn app.api:app"
sleep 2
# Restart
bash scripts/run_api.sh
```

### Problem: Page returns 404

**Cause:** Route not registered in `app/api.py`

**Solution:** Check that the route exists:
```python
# In app/api.py, should have:
@app.get("/total-core")
def total_core():
    return FileResponse(REPO_ROOT / "frontend" / "total-core.html")
```

### Problem: API endpoint returns 404

**Cause:** Router not included in `app/api.py`

**Solution:** Check router imports:
```python
# In app/api.py:
from app.routers.footprint import router as footprint_router
app.include_router(footprint_router)
```

### Problem: Import errors on startup

**Check logs:**
```bash
tail -50 server.log
```

**Common fixes:**
- Missing dependencies: `pip install <package>`
- Missing models: Check `app/models.py` for required classes

---

## File Reference

| File | Purpose |
|------|---------|
| `scripts/run_api.sh` | Start/restart API server |
| `scripts/run_jesse.sh` | Start/stop Jesse framework |
| `app/api.py` | Main FastAPI application |
| `app/routers/*.py` | API route handlers |
| `frontend/*.html` | Frontend pages |
| `frontend/*.js` | Frontend JavaScript |
| `server.log` | API server logs |

---

## Dependencies

### Python (in .venv)
```bash
pip install -e .
pip install apscheduler hmmlearn duckdb pandas_ta
```

### Required for Total Core
- SciChart.js (included in frontend/scichart/)
- Parquet data files in data/*_parquet/

### Required for Jesse
- Docker
- docker-compose

---

## What Was Missing (Historical Note)

On December 4, 2025, the following issues were identified and fixed:

1. **Missing page routes in `app/api.py`:**
   - `/total-core`
   - `/jesse`
   - `/backtest-lab`
   
2. **Missing API routers:**
   - `footprint_router`
   - `heatmap_router`
   - `trades_ws_router`
   - `orderbook_ws_router`

3. **Port configuration:**
   - Script was using port 8000 (occupied)
   - Changed to port 8001 in `scripts/run_api.sh`

**Fix applied:** Routes and routers added to `app/api.py`.

---

## Support

- **Logs**: `tail -f server.log`
- **API Docs**: http://localhost:8001/docs
- **OpenAPI**: http://localhost:8001/openapi.json
