/**
 * Total Core - Volume Profile / Footprint Chart
 * Uses SciChart.js for high-performance WebGL rendering
 */

// Import SciChart from the global namespace (loaded via script tag)
const {
    SciChartSurface,
    NumericAxis,
    DateTimeNumericAxis,
    FastCandlestickRenderableSeries,
    FastLineRenderableSeries,
    FastColumnRenderableSeries,
    FastMountainRenderableSeries,
    OhlcDataSeries,
    XyDataSeries,
    ZoomPanModifier,
    ZoomExtentsModifier,
    MouseWheelZoomModifier,
    RolloverModifier,
    CursorModifier,
    SciChartJsNavyTheme,
    NumberRange,
    EAutoRange,
    EAxisAlignment,
    ENumericFormat,
    LineAnnotation,
    BoxAnnotation,
    CustomAnnotation,
    TextAnnotation,
    ELabelPlacement,
    EAnnotationLayer,
    ECoordinateMode,
    EHorizontalAnchorPoint,
    EVerticalAnchorPoint,
    Thickness,
    // Heatmap imports for proper order book visualization
    UniformHeatmapRenderableSeries,
    UniformHeatmapDataSeries,
    HeatmapColorMap,
    zeroArray2D
} = SciChart;

// WebGL check removed - let SciChart handle initialization and fallbacks

// Configure WASM location
SciChartSurface.configure({
    wasmUrl: "/static/scichart/scichart2d.wasm",
    dataUrl: "/static/scichart/scichart2d.data"
});

// Custom Black Theme
const BLACK_THEME = {
    sciChartBackground: "#000000",
    loadingAnimationBackground: "#000000",
    loadingAnimationForeground: "#50C7E0",
    
    axisBorder: "transparent",
    axisTitleColor: "#888888",
    tickTextBrush: "#888888",
    
    majorGridLineBrush: "#1a1a1a",
    minorGridLineBrush: "#0d0d0d",
    
    gridBorderBrush: "#333333",
    
    axisBandsFill: "transparent",
    
    labelBackgroundBrush: "#000000cc",
    labelBorderBrush: "#333333",
    labelForegroundBrush: "#ffffff",
    
    cursorLineBrush: "#ffffff44",
    rolloverLineBrush: "#ffffff33",
    
    rubberBandFillBrush: "#ffffff11",
    rubberBandStrokeBrush: "#ffffff33",
    
    // Candlestick colors
    upBodyBrush: "#26a69a",
    downBodyBrush: "#ef5350",
    upWickColor: "#26a69a",
    downWickColor: "#ef5350",
    
    columnFillBrush: "#666666",
    columnLineColor: "#888888",
    
    lineSeriesColor: "#50C7E0"
};

// State
let mainSurface = null;
let indicatorSurface = null;
let wasmContext = null;
let indicatorContext = null;
let candleSeries = null;
let volumeSeries = null;
let deltaSeries = null;
let cvdSeries = null;
let profileAnnotations = [];
let bubbleAnnotations = [];  // Volume bubble annotations
let heatmapAnnotations = [];  // Liquidity heatmap annotations (fallback)
let heatmapSeries = null;    // SciChart UniformHeatmapRenderableSeries (proper 2D heatmap)
let currentData = null;
let bubbleData = null;  // Cached bubble data
let heatmapData = null;  // Cached heatmap depth data
let indicatorMode = 'delta'; // 'delta', 'cvd', 'cvd_line'

// Live order book streaming
let orderbookWebSocket = null;
let isRecording = false;  // Recording state (separate from heatmap display)
window.liveOrderBook = [];  // Global for heatmap rendering

/**
 * Connect to WebSocket for live order book streaming
 */
function connectOrderBookWebSocket() {
    if (orderbookWebSocket && orderbookWebSocket.readyState === WebSocket.OPEN) {
        console.log("OrderBook WebSocket already connected");
        return;
    }
    
    const wsUrl = `ws://${window.location.host}/api/orderbook/stream`;
    console.log(`Connecting to OrderBook WebSocket: ${wsUrl}`);
    
    orderbookWebSocket = new WebSocket(wsUrl);
    
    orderbookWebSocket.onopen = () => {
        console.log("OrderBook WebSocket connected");
        updateRecordStatus("Connected");
    };
    
    orderbookWebSocket.onmessage = (event) => {
        try {
            const msg = JSON.parse(event.data);
            
            if (msg.type === "status") {
                console.log("OrderBook status:", msg);
                if (!msg.running) {
                    updateHeatmapStatus("Stream not started - Click to start");
                }
            } else if (msg.type === "history") {
                window.liveOrderBook = msg.snapshots || [];
                console.log(`Received ${window.liveOrderBook.length} historical snapshots`);
                renderHeatmap();
            } else if (msg.type === "snapshot") {
                // Add new snapshot to rolling window
                window.liveOrderBook.push(msg.data);
                // Keep max 500 snapshots
                if (window.liveOrderBook.length > 500) {
                    window.liveOrderBook = window.liveOrderBook.slice(-500);
                }
                updateHeatmapStatus(`Live: ${window.liveOrderBook.length} snapshots`);
                // Re-render heatmap periodically (throttled)
                throttledRenderHeatmap();
            } else if (msg.type === "ping") {
                // Respond to keepalive
                orderbookWebSocket.send(JSON.stringify({command: "pong"}));
            }
        } catch (e) {
            console.error("OrderBook WebSocket message error:", e);
        }
    };
    
    orderbookWebSocket.onerror = (error) => {
        console.error("OrderBook WebSocket error:", error);
        updateHeatmapStatus("Connection error");
    };
    
    orderbookWebSocket.onclose = () => {
        console.log("OrderBook WebSocket closed");
        updateHeatmapStatus("Disconnected");
        orderbookWebSocket = null;
    };
}

/**
 * Disconnect from order book WebSocket
 */
function disconnectOrderBookWebSocket() {
    if (orderbookWebSocket) {
        orderbookWebSocket.close();
        orderbookWebSocket = null;
    }
    window.liveOrderBook = [];
}

/**
 * Start live order book streaming on the server
 */
async function startOrderBookStreaming() {
    try {
        updateHeatmapStatus("Starting stream...");
        const exchange = document.getElementById('exchange-select')?.value || 'binance';
        // Map frontend exchange name to CCXT exchange name
        const ccxtExchange = exchange === 'bybit' ? 'bybit' : 'binanceusdm';
        const symbol = exchange === 'bybit' ? 'BTC/USDT:USDT' : 'BTC/USDT:USDT';
        
        const resp = await fetch(`/api/orderbook/start?exchange=${ccxtExchange}&symbol=${encodeURIComponent(symbol)}`, {method: 'POST'});
        const data = await resp.json();
        if (data.error) {
            updateHeatmapStatus(`Error: ${data.error}`);
            console.error("Failed to start streaming:", data);
        } else {
            console.log("Streaming started:", data);
            updateHeatmapStatus("Stream started");
        }
    } catch (e) {
        console.error("Failed to start orderbook streaming:", e);
        updateHeatmapStatus("Failed to start");
    }
}

/**
 * Update heatmap status display
 */
function updateHeatmapStatus(status) {
    const display = document.getElementById('heatmap-opacity-display');
    if (display) {
        display.textContent = status;
    }
}

/**
 * Update record status display
 */
function updateRecordStatus(status) {
    const display = document.getElementById('record-status');
    if (display) {
        display.textContent = status;
        display.classList.toggle('active', isRecording);
    }
}

/**
 * Start recording order book data AND live trades
 */
async function startRecording() {
    isRecording = true;
    window.hasZoomedToLive = false;  // Reset zoom flag
    const btn = document.getElementById('record-btn');
    btn?.classList.add('recording');
    
    updateRecordStatus("Starting...");
    
    // Clear existing data for fresh live view
    if (candleSeries) candleSeries.dataSeries.clear();
    if (volumeSeries) volumeSeries.dataSeries.clear();
    if (deltaSeries) deltaSeries.dataSeries.clear();
    window.liveOrderBook = [];
    window.liveCandles = [];
    window.liveTrades = [];
    
    // Auto-enable heatmap visualization when recording
    const heatmapBtn = document.getElementById('show-heatmap');
    if (heatmapBtn && !heatmapBtn.classList.contains('active')) {
        heatmapBtn.classList.add('active');
        console.log("Auto-enabled heatmap for recording");
    }
    
    // Connect WebSocket for order book
    connectOrderBookWebSocket();
    
    // Connect WebSocket for trades  
    connectTradeWebSocket();
    
    // Start streaming on server (order book + trades)
    await Promise.all([
        startOrderBookStreaming(),
        startTradeStreaming()
    ]);
    
    updateRecordStatus("Recording");
    
    // Zoom to live price after a short delay to let data arrive
    setTimeout(() => {
        if (window.liveOrderBookMidPrice && !window.hasZoomedToLive) {
            zoomToLivePrice();
            window.hasZoomedToLive = true;
        }
    }, 1500);
}

/**
 * Stop recording order book data AND trades
 */
async function stopRecording() {
    isRecording = false;
    isTradeStreaming = false;
    const btn = document.getElementById('record-btn');
    btn?.classList.remove('recording');
    
    // Stop server streaming
    try {
        await Promise.all([
            fetch('/api/orderbook/stop', {method: 'POST'}),
            fetch('/api/trades/stop', {method: 'POST'})
        ]);
    } catch (e) {
        console.error("Failed to stop streaming:", e);
    }
    
    // Disconnect WebSockets
    disconnectOrderBookWebSocket();
    if (tradeWebSocket) {
        tradeWebSocket.close();
        tradeWebSocket = null;
    }
    
    updateRecordStatus("Stopped");
}

// Throttled heatmap render (max 2 times per second)
let lastHeatmapRender = 0;
function throttledRenderHeatmap() {
    const now = Date.now();
    if (now - lastHeatmapRender >= 500) {
        lastHeatmapRender = now;
        renderHeatmap();
        updateDOM();  // Also update DOM when we get new order book data
        
        // Auto-zoom to live price on first data if not yet zoomed
        if (window.liveOrderBookMidPrice && !window.hasZoomedToLive && isRecording) {
            zoomToLivePrice();
            window.hasZoomedToLive = true;
        }
    }
}

// Trade streaming WebSocket
let tradeWebSocket = null;
let isTradeStreaming = false;
window.liveTrades = [];
window.liveCandles = [];

/**
 * Connect to trade streaming WebSocket
 */
function connectTradeWebSocket() {
    if (tradeWebSocket && tradeWebSocket.readyState === WebSocket.OPEN) {
        return;
    }
    
    const wsUrl = `ws://${window.location.host}/api/trades/stream`;
    console.log(`Connecting to Trade WebSocket: ${wsUrl}`);
    
    tradeWebSocket = new WebSocket(wsUrl);
    
    tradeWebSocket.onopen = () => {
        console.log("Trade WebSocket connected");
    };
    
    tradeWebSocket.onmessage = (event) => {
        try {
            const msg = JSON.parse(event.data);
            
            if (msg.type === "trade") {
                // Individual trade - update current candle
                window.liveTrades.push(msg.data);
                if (window.liveTrades.length > 1000) {
                    window.liveTrades = window.liveTrades.slice(-1000);
                }
            } else if (msg.type === "current_candle") {
                // Update current candle display
                updateLiveCandle(msg.data);
            } else if (msg.type === "candle") {
                // Completed candle - add to chart
                addCompletedCandle(msg.data);
            } else if (msg.type === "candles") {
                // Initial batch of candles
                window.liveCandles = msg.data || [];
                console.log(`Received ${window.liveCandles.length} live candles`);
            }
        } catch (e) {
            console.error("Trade WebSocket message error:", e);
        }
    };
    
    tradeWebSocket.onerror = (error) => {
        console.error("Trade WebSocket error:", error);
    };
    
    tradeWebSocket.onclose = () => {
        console.log("Trade WebSocket closed");
        tradeWebSocket = null;
    };
}

/**
 * Start trade streaming on server
 */
async function startTradeStreaming() {
    try {
        const timeframe = document.getElementById('tf-select').value;
        const exchange = document.getElementById('exchange-select')?.value || 'binance';
        // Map frontend exchange name to CCXT exchange name
        const ccxtExchange = exchange === 'bybit' ? 'bybit' : 'binanceusdm';
        const symbol = exchange === 'bybit' ? 'BTC/USDT:USDT' : 'BTC/USDT:USDT';
        
        const tfMs = {
            "1m": 60000, "5m": 300000, "15m": 900000,
            "30m": 1800000, "1h": 3600000, "4h": 14400000
        };
        const candleInterval = tfMs[timeframe] || 60000;
        const binSize = parseFloat(document.getElementById('tick-size').value) || 1;
        
        const resp = await fetch(`/api/trades/start?exchange=${ccxtExchange}&symbol=${encodeURIComponent(symbol)}&candle_interval_ms=${candleInterval}&price_bucket_size=${binSize}`, {method: 'POST'});
        const data = await resp.json();
        if (data.error) {
            console.error("Failed to start trade streaming:", data);
        } else {
            console.log("Trade streaming started:", data);
            isTradeStreaming = true;
        }
    } catch (e) {
        console.error("Failed to start trade streaming:", e);
    }
}

/**
 * Update the DOM (Depth of Market) panel with current order book
 * Three-column layout: Bid Qty | Bid Bar | Price | Ask Bar | Ask Qty
 */
function updateDOM() {
    const asksContainer = document.getElementById('dom-asks');
    const bidsContainer = document.getElementById('dom-bids');
    const midPriceEl = document.getElementById('dom-mid-price');
    const spreadEl = document.getElementById('dom-spread');
    const aggSelect = document.getElementById('dom-aggregation');
    
    if (!asksContainer || !bidsContainer || !window.liveOrderBook || window.liveOrderBook.length === 0) {
        return;
    }
    
    // Get latest order book snapshot
    const latest = window.liveOrderBook[window.liveOrderBook.length - 1];
    if (!latest || !latest.bids || !latest.asks) return;
    
    // Get aggregation level
    const aggLevel = parseFloat(aggSelect?.value) || 5;
    
    // Aggregate order book by price buckets
    function aggregateOrders(orders, bucketSize, isBid) {
        const buckets = new Map();
        orders.forEach(([price, qty]) => {
            // Round to bucket
            const bucket = isBid 
                ? Math.floor(price / bucketSize) * bucketSize
                : Math.ceil(price / bucketSize) * bucketSize;
            buckets.set(bucket, (buckets.get(bucket) || 0) + qty);
        });
        return Array.from(buckets.entries()).sort((a, b) => isBid ? b[0] - a[0] : a[0] - b[0]);
    }
    
    const bids = aggregateOrders(latest.bids, aggLevel, true).slice(0, 40);
    const asks = aggregateOrders(latest.asks, aggLevel, false).slice(0, 40);
    
    if (bids.length === 0 || asks.length === 0) return;
    
    // Calculate mid price and spread
    const bestBid = bids[0][0];
    const bestAsk = asks[0][0];
    const midPrice = (bestBid + bestAsk) / 2;
    const spread = bestAsk - bestBid;
    
    midPriceEl.textContent = midPrice.toFixed(1);
    spreadEl.textContent = `$${spread.toFixed(2)}`;
    
    // Store mid price for chart alignment
    window.liveOrderBookMidPrice = midPrice;
    
    // Find max quantity for bar scaling
    const allQtys = [...bids.map(b => b[1]), ...asks.map(a => a[1])];
    const maxQty = Math.max(...allQtys);
    
    // Format quantity display
    const formatQty = (qty) => {
        if (qty >= 100) return Math.round(qty).toString();
        if (qty >= 10) return qty.toFixed(1);
        if (qty >= 1) return qty.toFixed(2);
        return qty.toFixed(3);
    };
    
    // Build a unified price ladder from bestBid down and bestAsk up
    // Each row shows: BidQty | BidBar | Price | AskBar | AskQty
    const bidMap = new Map(bids);
    const askMap = new Map(asks);
    
    // Build asks HTML - prices above mid (lowest ask at bottom)
    let asksHtml = '';
    asks.slice().reverse().forEach(([price, qty]) => {
        const barWidth = Math.min((qty / maxQty * 100), 100).toFixed(1);
        asksHtml += `
            <div class="dom-row">
                <span class="bid-qty"></span>
                <div class="bid-bar"></div>
                <span class="price">${price.toFixed(2)}</span>
                <div class="ask-bar"><div class="ask-bar-fill" style="width: ${barWidth}%"></div></div>
                <span class="ask-qty">${formatQty(qty)}</span>
            </div>
        `;
    });
    asksContainer.innerHTML = asksHtml;
    
    // Build bids HTML - prices below mid
    let bidsHtml = '';
    bids.forEach(([price, qty]) => {
        const barWidth = Math.min((qty / maxQty * 100), 100).toFixed(1);
        bidsHtml += `
            <div class="dom-row">
                <span class="bid-qty">${formatQty(qty)}</span>
                <div class="bid-bar"><div class="bid-bar-fill" style="width: ${barWidth}%"></div></div>
                <span class="price">${price.toFixed(2)}</span>
                <div class="ask-bar"></div>
                <span class="ask-qty"></span>
            </div>
        `;
    });
    bidsContainer.innerHTML = bidsHtml;
}

// Store historical order book data
let historicalOrderBook = null;

/**
 * Load historical order book snapshot for a given timestamp (for Bybit).
 * Fetches data for the visible price range on the chart.
 */
async function loadHistoricalOrderBook(timestamp) {
    const exchange = document.getElementById('exchange-select')?.value || 'binance';
    
    // Only Bybit has historical order book data
    if (exchange !== 'bybit') {
        console.log("Historical order book only available for Bybit");
        return null;
    }
    
    // Get visible price range from chart
    let priceMin = null, priceMax = null;
    if (mainSurface) {
        const yAxis = mainSurface.yAxes.get(0);
        if (yAxis && yAxis.visibleRange) {
            priceMin = Math.floor(yAxis.visibleRange.min);
            priceMax = Math.ceil(yAxis.visibleRange.max);
        }
    }
    
    try {
        let url = `/api/heatmap/bybit/orderbook/snapshot?timestamp=${timestamp}&levels=500`;
        if (priceMin !== null && priceMax !== null) {
            url += `&price_min=${priceMin}&price_max=${priceMax}`;
        }
        console.log(`Loading historical order book: ${url}`);
        const resp = await fetch(url);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        
        const data = await resp.json();
        if (data.error) {
            console.warn("No historical order book:", data.error);
            return null;
        }
        
        historicalOrderBook = data;
        historicalOrderBook.visiblePriceRange = { min: priceMin, max: priceMax };
        console.log(`Loaded historical order book: ${data.bids?.length} bids, ${data.asks?.length} asks`);
        return data;
    } catch (err) {
        console.error("Failed to load historical order book:", err);
        return null;
    }
}

/**
 * Update the DOM panel with historical order book data.
 * Shows the FULL order book - ALL levels from the data, aggregated by the selected price bucket.
 * The DOM should display the ENTIRE depth of the order book, not just a few levels.
 */
function updateDOMHistorical(orderBookData) {
    const asksContainer = document.getElementById('dom-asks');
    const bidsContainer = document.getElementById('dom-bids');
    const midPriceEl = document.getElementById('dom-mid-price');
    const spreadEl = document.getElementById('dom-spread');
    const aggSelect = document.getElementById('dom-aggregation');
    
    if (!asksContainer || !bidsContainer || !orderBookData) {
        return;
    }
    
    const { bids, asks, mid_price, spread } = orderBookData;
    if (!bids || !asks || bids.length === 0 || asks.length === 0) return;
    
    // Get aggregation level from dropdown
    const aggLevel = parseFloat(aggSelect?.value) || 1;
    
    // Aggregate bids by price bucket - KEEP ALL LEVELS
    const bidMap = new Map();
    bids.forEach(([price, qty]) => {
        const bucket = Math.floor(price / aggLevel) * aggLevel;
        bidMap.set(bucket, (bidMap.get(bucket) || 0) + qty);
    });
    
    // Aggregate asks by price bucket - KEEP ALL LEVELS
    const askMap = new Map();
    asks.forEach(([price, qty]) => {
        const bucket = Math.ceil(price / aggLevel) * aggLevel;
        askMap.set(bucket, (askMap.get(bucket) || 0) + qty);
    });
    
    // Get sorted price levels from the ACTUAL order book data
    const askPrices = [...askMap.keys()].sort((a, b) => a - b);  // Low to high
    const bidPrices = [...bidMap.keys()].sort((a, b) => b - a);  // High to low
    
    // Update mid price and spread display
    midPriceEl.textContent = mid_price.toFixed(1);
    if (spreadEl) spreadEl.textContent = `$${spread.toFixed(2)}`;
    
    // Find max quantity for bar scaling (use 90th percentile)
    const allQtys = [...bidMap.values(), ...askMap.values()].sort((a, b) => a - b);
    const maxQty = allQtys.length > 0 ? allQtys[Math.floor(allQtys.length * 0.9)] || 1 : 1;
    
    // Format quantity display
    const formatQty = (qty) => {
        if (qty === 0) return '';
        if (qty >= 100) return Math.round(qty).toString();
        if (qty >= 10) return qty.toFixed(1);
        if (qty >= 1) return qty.toFixed(2);
        return qty.toFixed(3);
    };
    
    // Build asks HTML - ALL ask levels (lowest at bottom near mid, highest at top)
    // Reverse so highest is at top of the container
    let asksHtml = '';
    const displayAskPrices = askPrices.slice().reverse();  // Highest at top
    displayAskPrices.forEach(price => {
        const qty = askMap.get(price) || 0;
        const barWidth = Math.min((qty / maxQty * 100), 100).toFixed(1);
        const qtyDisplay = formatQty(qty);
        const isHighlight = qty > maxQty * 0.7 ? ' highlight' : '';
        asksHtml += `
            <div class="dom-row${isHighlight}">
                <span class="bid-qty"></span>
                <div class="bid-bar"></div>
                <span class="price">${price.toFixed(2)}</span>
                <div class="ask-bar"><div class="ask-bar-fill" style="width: ${barWidth}%"></div></div>
                <span class="ask-qty">${qtyDisplay}</span>
            </div>
        `;
    });
    asksContainer.innerHTML = asksHtml;
    
    // Build bids HTML - ALL bid levels (highest at top near mid, lowest at bottom)
    let bidsHtml = '';
    bidPrices.forEach(price => {
        const qty = bidMap.get(price) || 0;
        const barWidth = Math.min((qty / maxQty * 100), 100).toFixed(1);
        const qtyDisplay = formatQty(qty);
        const isHighlight = qty > maxQty * 0.7 ? ' highlight' : '';
        bidsHtml += `
            <div class="dom-row${isHighlight}">
                <span class="bid-qty">${qtyDisplay}</span>
                <div class="bid-bar"><div class="bid-bar-fill" style="width: ${barWidth}%"></div></div>
                <span class="price">${price.toFixed(2)}</span>
                <div class="ask-bar"></div>
                <span class="ask-qty"></span>
            </div>
        `;
    });
    bidsContainer.innerHTML = bidsHtml;
    
    console.log(`DOM: ${askPrices.length} asks, ${bidPrices.length} bids (total ${bids.length}/${asks.length} raw levels), agg $${aggLevel}`);
}

/**
 * Zoom chart to current live price
 */
function zoomToLivePrice() {
    if (!mainSurface || !window.liveOrderBookMidPrice) return;
    
    const price = window.liveOrderBookMidPrice;
    const yAxis = mainSurface.yAxes.get(0);
    const xAxis = mainSurface.xAxes.get(0);
    
    if (yAxis && price > 0) {
        // Set Y axis to show $500 range around current price
        const range = 250;
        yAxis.visibleRange = new NumberRange(price - range, price + range);
        console.log(`Zoomed Y to: $${(price - range).toFixed(0)} - $${(price + range).toFixed(0)}`);
    }
    
    if (xAxis) {
        // Set X axis to show last 30 minutes
        const now = Date.now() / 1000;
        const thirtyMinsAgo = now - (30 * 60);
        xAxis.visibleRange = new NumberRange(thirtyMinsAgo, now + 60);
        console.log(`Zoomed X to last 30 mins`);
    }
}

/**
 * Update the current live candle on the chart in real-time
 */
function updateLiveCandle(candleData) {
    window.currentLiveCandle = candleData;
    
    if (!candleSeries || !mainSurface) return;
    
    const ds = candleSeries.dataSeries;
    const timestampSec = candleData.timestamp / 1000;
    
    // Check if we need to update the last candle or add a new one
    const count = ds.count();
    if (count === 0) {
        // First candle - append it
        ds.append(timestampSec, candleData.open, candleData.high, candleData.low, candleData.close);
        console.log("Added first live candle at", new Date(candleData.timestamp).toISOString());
    } else {
        const lastX = ds.getNativeXValues().get(count - 1);
        
        // If same timestamp, update in place; otherwise append new
        if (Math.abs(lastX - timestampSec) < 30) {  // Within 30 seconds = same candle
            // Update the existing candle
            ds.update(count - 1, candleData.open, candleData.high, candleData.low, candleData.close);
        } else {
            // New candle
            ds.append(timestampSec, candleData.open, candleData.high, candleData.low, candleData.close);
            console.log("Added new live candle at", new Date(candleData.timestamp).toISOString());
            
            // Keep chart scrolled to show latest
            const xAxis = mainSurface.xAxes.get(0);
            if (xAxis) {
                const visibleRange = xAxis.visibleRange;
                const rangeWidth = visibleRange.max - visibleRange.min;
                // Shift view to include new candle
                if (timestampSec > visibleRange.max - 60) {
                    xAxis.visibleRange = new NumberRange(timestampSec - rangeWidth + 120, timestampSec + 120);
                }
            }
        }
    }
    
    // Also update volume if we have volume data
    if (volumeSeries && candleData.volume !== undefined) {
        const vds = volumeSeries.dataSeries;
        const vcount = vds.count();
        if (vcount === 0) {
            vds.append(timestampSec, candleData.volume);
        } else {
            const lastVX = vds.getNativeXValues().get(vcount - 1);
            if (Math.abs(lastVX - timestampSec) < 30) {
                vds.update(vcount - 1, timestampSec, candleData.volume);
            } else {
                vds.append(timestampSec, candleData.volume);
            }
        }
    }
}

/**
 * Add a completed candle to the chart
 */
function addCompletedCandle(candleData) {
    window.liveCandles.push(candleData);
    
    if (!candleSeries || !mainSurface) return;
    
    const ds = candleSeries.dataSeries;
    const timestampSec = candleData.timestamp / 1000;
    
    // Append the completed candle
    ds.append(timestampSec, candleData.open, candleData.high, candleData.low, candleData.close);
    
    if (volumeSeries && candleData.volume !== undefined) {
        volumeSeries.dataSeries.append(timestampSec, candleData.volume);
    }
    
    console.log("Completed candle:", new Date(candleData.timestamp).toISOString(), "close:", candleData.close);
}
let showVolumeInUSD = true;  // Default to USD for better visual comparison
let avgPrice = 0;  // Average price for USD conversion
let cachedATR = null;  // Cached ATR for auto-binning

/**
 * Calculate Average True Range (ATR) from candle data
 * Used for adaptive bin sizing based on volatility
 */
function calculateATR(candles, period = 14) {
    if (!candles || candles.length < 2) return null;
    
    const trueRanges = [];
    for (let i = 1; i < candles.length; i++) {
        const high = candles[i].high;
        const low = candles[i].low;
        const prevClose = candles[i - 1].close;
        
        const tr = Math.max(
            high - low,
            Math.abs(high - prevClose),
            Math.abs(low - prevClose)
        );
        trueRanges.push(tr);
    }
    
    // Use simple average for initial ATR calculation
    const lookback = Math.min(period, trueRanges.length);
    const recentTRs = trueRanges.slice(-lookback);
    const atr = recentTRs.reduce((a, b) => a + b, 0) / recentTRs.length;
    
    return atr;
}

/**
 * Calculate optimal bin size based on ATR
 * Formula: bin = round(ATR * 0.15) clamped between min and max values
 */
function getATRBasedBinSize(atr, timeframe) {
    if (!atr || atr <= 0) return null;
    
    // Scale factor varies by timeframe (higher TF = larger bins)
    const tfMultiplier = {
        "1m": 0.08, "5m": 0.12, "15m": 0.15, "30m": 0.18,
        "1h": 0.20, "4h": 0.25, "1d": 0.30
    };
    const multiplier = tfMultiplier[timeframe] || 0.15;
    
    // Calculate raw bin size
    let binSize = Math.round(atr * multiplier);
    
    // Clamp to reasonable values
    const minBin = { "1m": 1, "5m": 1, "15m": 2, "30m": 3, "1h": 5, "4h": 10, "1d": 20 };
    const maxBin = { "1m": 10, "5m": 20, "15m": 50, "30m": 100, "1h": 200, "4h": 500, "1d": 1000 };
    
    binSize = Math.max(binSize, minBin[timeframe] || 1);
    binSize = Math.min(binSize, maxBin[timeframe] || 100);
    
    return binSize;
}

// Colors
const COLORS = {
    up: '#26a69a',
    down: '#ef5350',
    poc: '#ffd700',
    vah: '#4caf50',
    val: '#f44336',
    buyProfile: '#26a69a88',
    sellProfile: '#ef535088',
    neutral: '#666666'
};

async function initSciChart() {
    try {
        // 1. Main Price Chart with black theme
        const result = await SciChartSurface.create("sci-chart-div", {
            theme: BLACK_THEME
        });
        mainSurface = result.sciChartSurface;
        wasmContext = result.wasmContext;

        // Set sensible initial ranges for BTC chart
        // X Axis: Last 2 hours from now
        const now = Date.now() / 1000;
        const twoHoursAgo = now - (2 * 60 * 60);
        
        // X Axis - DateTime for proper date labels (inside chart to maximize space)
        const xAxis = new DateTimeNumericAxis(wasmContext, {
            axisAlignment: EAxisAlignment.Bottom,
            drawLabels: true,
            drawMinorGridLines: false,
            labelFormat: ENumericFormat.DateTimeNumeric,
            cursorLabelFormat: ENumericFormat.DateTimeNumeric,
            isInnerAxis: true,  // Draw labels inside chart area
            axisBorder: { borderTop: 0, color: "transparent" },
            visibleRange: new NumberRange(twoHoursAgo, now + 300)  // Initial: last 2 hours + 5 min buffer
        });

        // Y Axis - Price (inside chart to maximize space)
        // Start with sensible BTC range, will auto-adjust when data loads
        const yAxis = new NumericAxis(wasmContext, {
            axisAlignment: EAxisAlignment.Right,
            autoRange: EAutoRange.Never,  // We'll control range manually
            growBy: new NumberRange(0.05, 0.15),
            visibleRange: new NumberRange(90000, 95000),  // Initial BTC range ~$90-95k
            labelPrefix: "$",
            labelPrecision: 0,
            isInnerAxis: true,  // Draw labels inside chart area
            axisBorder: { borderLeft: 0, color: "transparent" }
        });

        // Volume Axis (hidden, for volume bars at bottom)
        const volAxis = new NumericAxis(wasmContext, {
            id: "volAxis",
            axisAlignment: EAxisAlignment.Left,
            isVisible: false,
            autoRange: EAutoRange.Always,
            growBy: new NumberRange(0, 4) // Only use bottom 25% of chart
        });

        mainSurface.xAxes.add(xAxis);
        mainSurface.yAxes.add(yAxis);
        mainSurface.yAxes.add(volAxis);

        // Modifiers
        mainSurface.chartModifiers.add(
            new ZoomPanModifier(),
            new MouseWheelZoomModifier(),
            new ZoomExtentsModifier({ isAnimated: true }),
            new CursorModifier({ showTooltip: true, showAxisLabels: true })
        );

        // Candlestick Series
        candleSeries = new FastCandlestickRenderableSeries(wasmContext, {
            dataSeries: new OhlcDataSeries(wasmContext, { dataSeriesName: "OHLC" }),
            strokeThickness: 1,
            dataPointWidth: 0.7,
            brushUp: COLORS.up,
            brushDown: COLORS.down,
            strokeUp: COLORS.up,
            strokeDown: COLORS.down
        });
        mainSurface.renderableSeries.add(candleSeries);

        // Volume Bars - hidden by default (CVD is below)
        volumeSeries = new FastColumnRenderableSeries(wasmContext, {
            dataSeries: new XyDataSeries(wasmContext, { dataSeriesName: "Volume" }),
            yAxisId: "volAxis",
            strokeThickness: 0,
            dataPointWidth: 0.6,
            opacity: 0,  // Hidden - use CVD chart instead
            fill: COLORS.neutral,
            isVisible: false  // Hide volume from main chart
        });
        mainSurface.renderableSeries.add(volumeSeries);

        // Add listener for Y-axis visible range changes to update DOM panel and heatmap
        // This makes the DOM panel show all prices in the visible chart area
        // and re-renders the canvas heatmap to match the new visible range
        let domUpdateTimeout = null;
        let heatmapUpdateTimeout = null;
        
        const onVisibleRangeChanged = () => {
            // Debounce DOM update
            if (domUpdateTimeout) clearTimeout(domUpdateTimeout);
            domUpdateTimeout = setTimeout(() => {
                const exchange = document.getElementById('exchange-select')?.value || 'binance';
                if (exchange === 'bybit' && historicalOrderBook) {
                    updateDOMHistorical(historicalOrderBook);
                }
            }, 150);
            
            // Debounce heatmap re-render (canvas needs to sync with chart)
            if (heatmapUpdateTimeout) clearTimeout(heatmapUpdateTimeout);
            heatmapUpdateTimeout = setTimeout(() => {
                const showHeatmap = document.getElementById('show-heatmap')?.classList.contains('active') ?? false;
                if (showHeatmap && heatmapData && heatmapData.data?.length > 0) {
                    renderBybitHistoricalHeatmap(heatmapData.data);
                }
            }, 100);  // Faster re-render for smooth feel
        };
        
        yAxis.visibleRangeChanged.subscribe(onVisibleRangeChanged);
        xAxis.visibleRangeChanged.subscribe(onVisibleRangeChanged);
        
        console.log("SciChart initialized successfully");
        return true;

    } catch (e) {
        console.error("Failed to initialize SciChart:", e);
        document.getElementById('loading').innerHTML = `
            <div style="color: red; text-align: center;">
                <p>Failed to initialize chart engine</p>
                <p style="font-size: 12px;">${e.message}</p>
            </div>
        `;
        return false;
    }
}

async function initIndicatorChart() {
    try {
        const result = await SciChartSurface.create("indicator-chart-div", {
            theme: BLACK_THEME
        });
        indicatorSurface = result.sciChartSurface;
        indicatorContext = result.wasmContext;

        // X Axis - DateTime synced with main chart (inside chart)
        const xAxis = new DateTimeNumericAxis(indicatorContext, {
            axisAlignment: EAxisAlignment.Bottom,
            drawLabels: false,
            drawMinorGridLines: false,
            isInnerAxis: true
        });

        // Y Axis - Delta/CVD (inside chart)
        const yAxis = new NumericAxis(indicatorContext, {
            axisAlignment: EAxisAlignment.Right,
            autoRange: EAutoRange.Always,
            growBy: new NumberRange(0.1, 0.1),
            axisTitle: "Delta",
            isInnerAxis: true,
            axisBorder: { borderLeft: 0, color: "transparent" }
        });

        indicatorSurface.xAxes.add(xAxis);
        indicatorSurface.yAxes.add(yAxis);

        // Delta histogram (bars)
        deltaSeries = new FastColumnRenderableSeries(indicatorContext, {
            dataSeries: new XyDataSeries(indicatorContext, { dataSeriesName: "Delta" }),
            strokeThickness: 0,
            dataPointWidth: 0.7
        });
        indicatorSurface.renderableSeries.add(deltaSeries);

        // CVD line (hidden by default)
        cvdSeries = new FastLineRenderableSeries(indicatorContext, {
            dataSeries: new XyDataSeries(indicatorContext, { dataSeriesName: "CVD" }),
            stroke: "#50C7E0",
            strokeThickness: 2,
            isVisible: false
        });
        indicatorSurface.renderableSeries.add(cvdSeries);

        // Modifiers - no zoom/pan, synced from main chart
        // We'll sync manually via visibleRangeChanged

        console.log("Indicator chart initialized");
        
        // Sync X-axis with main chart when main chart visible range changes
        if (mainSurface && mainSurface.xAxes.get(0)) {
            mainSurface.xAxes.get(0).visibleRangeChanged.subscribe((args) => {
                if (indicatorSurface && indicatorSurface.xAxes.get(0)) {
                    indicatorSurface.xAxes.get(0).visibleRange = args.visibleRange;
                }
            });
        }
    } catch (e) {
        console.error("Failed to initialize indicator chart:", e);
    }
}

async function loadData() {
    const symbol = document.getElementById('symbol-select').value;
    const exchange = document.getElementById('exchange-select')?.value || 'binance';
    const timeframe = document.getElementById('tf-select').value;
    const limit = parseInt(document.getElementById('candle-limit').value) || 100;
    
    // Bin size = tick_size (the input value directly represents $ per price bin)
    // ticks_per_row is now always 1 since we've renamed the control to "Bin Size"
    // This makes it simpler: Bin Size $1 = each row is $1 wide
    const fallbackBinSize = {
        "1m": 1, "5m": 2, "15m": 3, "30m": 5, "1h": 10, "4h": 20, "1d": 50
    };
    const tickSizeInput = document.getElementById('tick-size');
    
    // Auto-adjust bin size: prefer ATR-based, fallback to fixed values
    if (!tickSizeInput.dataset.userSet) {
        const atrBin = cachedATR ? getATRBasedBinSize(cachedATR, timeframe) : null;
        tickSizeInput.value = atrBin || fallbackBinSize[timeframe] || 5;
        console.log(`Auto bin size: ATR=${cachedATR?.toFixed(1)}, bin=$${tickSizeInput.value}`);
    }
    
    // Read the (possibly auto-adjusted) value
    const binSize = parseFloat(tickSizeInput.value) || fallbackBinSize[timeframe] || 5;
    
    // Now we send tick_size=binSize and ticks_per_row=1 so the API gives us exactly $binSize per row
    const tickSize = binSize;
    const ticksPerRow = 1;
    
    // Show actual bin size in the display span
    const binDisplay = document.getElementById('bin-size-display');
    if (binDisplay) {
        binDisplay.textContent = `= $${binSize}/row`;
    }
    
    // Check for specific start date/time (separate inputs)
    const startDateInput = document.getElementById('start-date');
    const startTimeInput = document.getElementById('start-time-clock');
    let startTs = null;
    let endTs = null;
    
    if (startDateInput && startDateInput.value) {
        const timeValue = startTimeInput?.value || '00:00';
        const dateTimeStr = `${startDateInput.value}T${timeValue}`;
        const startDate = new Date(dateTimeStr);
        startTs = startDate.getTime();
        console.log(`Loading from: ${dateTimeStr} (ts=${startTs})`);
        // Calculate end based on limit and timeframe
        const tfMs = {
            "1m": 60_000, "5m": 300_000, "15m": 900_000,
            "30m": 1_800_000, "1h": 3_600_000, "4h": 14_400_000, "1d": 86_400_000
        };
        endTs = startTs + (limit * tfMs[timeframe]);
    }

    document.getElementById('loading').style.display = 'flex';
    document.getElementById('loading-text').textContent = `Loading ${limit} candles...`;

    try {
        let url = `/api/footprint/candles?symbol=${symbol}&exchange=${exchange}&timeframe=${timeframe}&tick_size=${tickSize}&ticks_per_row=${ticksPerRow}&limit=${limit}`;
        
        // Add timestamp parameters if specified
        if (startTs && endTs) {
            url += `&start_ts=${startTs}&end_ts=${endTs}`;
        }
        console.log("Fetching:", url);
        
        const response = await fetch(url);
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }
        
        const data = await response.json();
        console.log(`Loaded ${data.candles.length} candles for ${timeframe}`);
        
        // Calculate and cache ATR for future auto-binning
        const newATR = calculateATR(data.candles);
        if (newATR) {
            cachedATR = newATR;
            console.log(`ATR(14) = $${cachedATR.toFixed(2)}`);
        }
        
        currentData = data;
        renderData(data);
        updateStats(data);
        
        // For Bybit: Load historical order book for DOM panel (always, for the last candle)
        if (exchange === 'bybit' && data.candles?.length > 0) {
            const lastCandle = data.candles[data.candles.length - 1];
            const orderBook = await loadHistoricalOrderBook(lastCandle.timestamp);
            if (orderBook) {
                updateDOMHistorical(orderBook);
            }
        }
        
        // Load heatmap data (historical) if toggle is active
        const showHeatmap = document.getElementById('show-heatmap')?.classList.contains('active') ?? false;
        if (showHeatmap && data.candles?.length > 0) {
            await loadHeatmap(data.candles);
            renderHeatmap();
        }
        
        // Load bubbles if toggle is active
        const showBubbles = document.getElementById('show-bubbles')?.classList.contains('active') ?? false;
        if (showBubbles && data.candles?.length > 0) {
            await loadBubbles(data.candles);
            renderBubbles();
        }
        
    } catch (e) {
        console.error("Load error:", e);
        document.getElementById('loading-text').textContent = `Error: ${e.message}`;
        setTimeout(() => {
            document.getElementById('loading').style.display = 'none';
        }, 2000);
        return;
    }
    
    document.getElementById('loading').style.display = 'none';
}

function renderData(data) {
    if (!mainSurface || !candleSeries) {
        console.error("Chart not initialized");
        return;
    }

    const { candles, timeframe } = data;
    
    // Get toggle states
    const showFootprints = document.getElementById('show-footprint')?.classList.contains('active') ?? true;
    const showOrderFlow = document.getElementById('show-orderflow')?.classList.contains('active') ?? false;
    const showPOC = document.getElementById('show-poc')?.classList.contains('active') ?? true;
    const showVA = document.getElementById('show-va')?.classList.contains('active') ?? false;
    
    // Calculate average price for USD conversion
    if (candles.length > 0) {
        avgPrice = candles.reduce((sum, c) => sum + (c.high + c.low) / 2, 0) / candles.length;
    }
    
    // Volume formatting function with USD support
    const formatVol = (volBTC) => {
        if (showVolumeInUSD && avgPrice > 0) {
            const volUSD = volBTC * avgPrice;
            if (volUSD >= 1_000_000) return (volUSD / 1_000_000).toFixed(1) + 'M';
            if (volUSD >= 1_000) return (volUSD / 1_000).toFixed(0) + 'K';
            return Math.round(volUSD).toString();
        } else {
            if (volBTC >= 1000) return (volBTC / 1000).toFixed(1) + 'k';
            if (volBTC >= 100) return Math.round(volBTC).toString();
            if (volBTC >= 10) return volBTC.toFixed(1);
            return volBTC.toFixed(2);
        }
    };
    
    // Clear existing data
    candleSeries.dataSeries.clear();
    volumeSeries.dataSeries.clear();
    if (deltaSeries) deltaSeries.dataSeries.clear();
    if (cvdSeries) cvdSeries.dataSeries.clear();
    
    // Clear annotations
    profileAnnotations.forEach(a => mainSurface.annotations.remove(a));
    profileAnnotations = [];

    // Prepare data arrays
    // DateTimeNumericAxis expects Unix timestamps in SECONDS
    const xValues = [];
    const openValues = [];
    const highValues = [];
    const lowValues = [];
    const closeValues = [];
    const volumeValues = [];
    const deltaValues = [];
    const cvdValues = [];
    
    let cumulativeDelta = 0;
    
    // Get candle width in seconds for annotations
    const tfMs = {
        "1m": 60_000, "5m": 300_000, "15m": 900_000,
        "30m": 1_800_000, "1h": 3_600_000, "4h": 14_400_000, "1d": 86_400_000
    };
    const candleWidthMs = tfMs[timeframe] || 300_000;
    const candleWidthSec = candleWidthMs / 1000;

    candles.forEach((candle, i) => {
        // Convert ms to seconds for DateTimeNumericAxis
        const timestampSec = candle.timestamp / 1000;
        
        xValues.push(timestampSec);
        openValues.push(candle.open);
        highValues.push(candle.high);
        lowValues.push(candle.low);
        closeValues.push(candle.close);
        volumeValues.push(candle.volume);
        deltaValues.push(candle.total_delta);
        
        // Calculate CVD
        cumulativeDelta += candle.total_delta;
        cvdValues.push(cumulativeDelta);

        // Render footprint cells - proper footprint chart style
        // Background: Green=Ask>Bid, Purple=Bid>Ask, Gray=balanced
        // Text: Black default, Blue=buy imbalance 200%+, Pink=sell imbalance 200%+
        // POC: Yellow border
        if (candle.profiles && candle.profiles.length > 0 && showFootprints) {
            const tickSize = data.tick_size * data.ticks_per_row;
            const cellWidth = candleWidthSec * 0.95;
            
            // Smart rendering: limit profiles when zoomed out (too many candles)
            // This prevents performance issues without losing data
            const maxProfilesPerCandle = data.candles.length > 100 ? 8 : 
                                         data.candles.length > 50 ? 15 : 
                                         data.candles.length > 20 ? 25 : 999;
            
            // Sort profiles by price for diagonal imbalance calculation
            let sortedProfiles = [...candle.profiles].sort((a, b) => a.price - b.price);
            
            // If too many profiles, keep POC area + top volume profiles
            if (sortedProfiles.length > maxProfilesPerCandle) {
                // Sort by volume to find most important levels
                const byVolume = [...sortedProfiles].sort((a, b) => b.total_volume - a.total_volume);
                const topProfiles = new Set(byVolume.slice(0, maxProfilesPerCandle).map(p => p.price));
                // Always include POC
                if (candle.poc) topProfiles.add(candle.poc);
                // Filter and re-sort by price
                sortedProfiles = sortedProfiles.filter(p => topProfiles.has(p.price));
            }
            
            sortedProfiles.forEach((profile, idx) => {
                const priceY = profile.price;
                const bidVol = Math.round(profile.sell_volume);  // Bid = sellers hitting bid
                const askVol = Math.round(profile.buy_volume);   // Ask = buyers lifting ask
                const isPOC = candle.poc && Math.abs(priceY - candle.poc) < tickSize / 2;
                const totalVol = bidVol + askVol;
                const horizontalDelta = askVol - bidVol;
                
                // === BACKGROUND COLOR (horizontal delta at same level) ===
                // GREEN = more buying (Ask > Bid), PURPLE = more selling (Bid > Ask)
                // Use LIGHT PASTEL colors like reference for dark text visibility
                let cellBg;
                
                if (totalVol === 0) {
                    cellBg = "#888899";  // Empty cell - light gray
                } else {
                    const imbalanceRatio = Math.abs(horizontalDelta) / totalVol;
                    
                    if (imbalanceRatio < 0.15) {
                        // Balanced - neutral light gray
                        cellBg = "#9a9aaa";
                    } else if (horizontalDelta > 0) {
                        // More ask (buying) - LIGHT GREEN pastel
                        const intensity = Math.min(imbalanceRatio * 1.2, 1);
                        const r = Math.round(140 - intensity * 40);
                        const g = Math.round(200 + intensity * 40);
                        const b = Math.round(140 - intensity * 20);
                        cellBg = `#${r.toString(16).padStart(2,'0')}${g.toString(16).padStart(2,'0')}${b.toString(16).padStart(2,'0')}`;
                    } else {
                        // More bid (selling) - LIGHT PURPLE/PINK pastel
                        const intensity = Math.min(imbalanceRatio * 1.2, 1);
                        const r = Math.round(200 + intensity * 40);
                        const g = Math.round(140 - intensity * 30);
                        const b = Math.round(200 + intensity * 40);
                        cellBg = `#${r.toString(16).padStart(2,'0')}${g.toString(16).padStart(2,'0')}${b.toString(16).padStart(2,'0')}`;
                    }
                }
                
                // === TEXT COLORS (diagonal imbalance - 200% threshold) ===
                // Default: BLACK on light backgrounds, or adapt to background
                // Imbalanced: CYAN for buy imbalance, MAGENTA for sell imbalance
                let bidTextColor = "#1a1a1a";  // Default dark text
                let askTextColor = "#1a1a1a";
                
                // Check bid imbalance: compare bid[i] with ask[i-1] (level below)
                if (idx > 0 && bidVol > 0) {
                    const askBelow = Math.round(sortedProfiles[idx - 1].buy_volume);
                    if (askBelow > 0 && bidVol >= askBelow * 2) {
                        // Strong sell imbalance - PINK/MAGENTA text
                        bidTextColor = "#ff00ff";
                    }
                }
                
                // Check ask imbalance: compare ask[i] with bid[i+1] (level above)
                if (idx < sortedProfiles.length - 1 && askVol > 0) {
                    const bidAbove = Math.round(sortedProfiles[idx + 1].sell_volume);
                    if (bidAbove > 0 && askVol >= bidAbove * 2) {
                        // Strong buy imbalance - BLUE/CYAN text
                        askTextColor = "#00bfff";
                    }
                }
                
                // === CELL BORDER ===
                const cellBorder = isPOC ? "#ffff00" : "#444444";
                const borderThickness = isPOC ? 2 : 1;
                
                // Calculate half-widths for two-column layout
                const halfCellWidth = cellWidth / 2;
                const bidX1 = timestampSec - cellWidth / 2;
                const bidX2 = timestampSec;  // Center divider
                const askX1 = timestampSec;
                const askX2 = timestampSec + cellWidth / 2;
                
                // Create BID box (left column) - uses same background but we'll color code
                const bidBox = new BoxAnnotation({
                    x1: bidX1,
                    y1: priceY,
                    x2: bidX2,
                    y2: priceY + tickSize,
                    fill: cellBg,
                    stroke: cellBorder,
                    strokeThickness: borderThickness,
                    annotationLayer: EAnnotationLayer.BelowChart
                });
                mainSurface.annotations.add(bidBox);
                profileAnnotations.push(bidBox);
                
                // Create ASK box (right column)
                const askBox = new BoxAnnotation({
                    x1: askX1,
                    y1: priceY,
                    x2: askX2,
                    y2: priceY + tickSize,
                    fill: cellBg,
                    stroke: cellBorder,
                    strokeThickness: borderThickness,
                    annotationLayer: EAnnotationLayer.BelowChart
                });
                mainSurface.annotations.add(askBox);
                profileAnnotations.push(askBox);
                
                // Center divider line for visual separation
                const dividerLine = new LineAnnotation({
                    x1: timestampSec,
                    y1: priceY,
                    x2: timestampSec,
                    y2: priceY + tickSize,
                    stroke: "#666666",
                    strokeThickness: 1,
                    annotationLayer: EAnnotationLayer.AboveChart
                });
                mainSurface.annotations.add(dividerLine);
                profileAnnotations.push(dividerLine);
                
                // Dynamic font size based on candle count - bigger fonts when zoomed in
                const fontSize = data.candles.length > 100 ? 9 : 
                                 data.candles.length > 50 ? 11 : 
                                 data.candles.length > 20 ? 12 :
                                 data.candles.length > 10 ? 14 : 16;
                
                // BID text (left column) - centered in left half
                const bidText = new TextAnnotation({
                    x1: bidX1 + halfCellWidth / 2,
                    y1: priceY + tickSize / 2,
                    text: formatVol(bidVol),
                    fontSize: fontSize,
                    fontFamily: "Arial",
                    textColor: bidTextColor,
                    horizontalAnchorPoint: EHorizontalAnchorPoint.Center,
                    verticalAnchorPoint: EVerticalAnchorPoint.Center,
                    annotationLayer: EAnnotationLayer.AboveChart
                });
                mainSurface.annotations.add(bidText);
                profileAnnotations.push(bidText);
                
                // ASK text (right column) - centered in right half  
                const askText = new TextAnnotation({
                    x1: askX1 + halfCellWidth / 2,
                    y1: priceY + tickSize / 2,
                    text: formatVol(askVol),
                    fontSize: fontSize,
                    fontFamily: "Arial",
                    textColor: askTextColor,
                    horizontalAnchorPoint: EHorizontalAnchorPoint.Center,
                    verticalAnchorPoint: EVerticalAnchorPoint.Center,
                    annotationLayer: EAnnotationLayer.AboveChart
                });
                mainSurface.annotations.add(askText);
                profileAnnotations.push(askText);
            });
        }
        
        // === ORDER FLOW VIEW: Horizontal volume bars extending from center vertical line ===
        // Only show Order Flow when Footprint is NOT active (mutually exclusive)
        if (candle.profiles && candle.profiles.length > 0 && showOrderFlow && !showFootprints) {
            const tickSize = data.tick_size * data.ticks_per_row;
            
            // Find max volume in this candle for bar width scaling
            const maxVol = Math.max(...candle.profiles.map(p => p.total_volume));
            if (maxVol === 0) return;
            
            // Find price range for this candle's profiles
            const minPrice = Math.min(...candle.profiles.map(p => p.price));
            const maxPrice = Math.max(...candle.profiles.map(p => p.price));
            
            // Draw VERTICAL CENTER LINE (like reference image)
            const centerLine = new LineAnnotation({
                x1: timestampSec,
                y1: minPrice,
                x2: timestampSec,
                y2: maxPrice + tickSize,
                stroke: "#8888ff",  // Blue/purple like reference
                strokeThickness: 2,
                annotationLayer: EAnnotationLayer.BelowChart
            });
            mainSurface.annotations.add(centerLine);
            profileAnnotations.push(centerLine);
            
            // Bars extend from CENTER to RIGHT only
            // Max bar width = 45% of candle width
            const maxBarWidth = candleWidthSec * 0.45;
            
            // Dynamic font sizing: fewer candles = larger fonts
            const fontSize = data.candles.length > 100 ? 8 : 
                             data.candles.length > 50 ? 10 : 
                             data.candles.length > 20 ? 12 :
                             data.candles.length > 10 ? 14 : 16;
            
            // Smart rendering: limit profiles when zoomed out
            const maxProfilesPerCandle = data.candles.length > 100 ? 10 : 
                                         data.candles.length > 50 ? 20 : 
                                         data.candles.length > 20 ? 30 : 999;
            
            let sortedProfiles = [...candle.profiles].sort((a, b) => a.price - b.price);
            
            if (sortedProfiles.length > maxProfilesPerCandle) {
                const byVolume = [...sortedProfiles].sort((a, b) => b.total_volume - a.total_volume);
                const topProfiles = new Set(byVolume.slice(0, maxProfilesPerCandle).map(p => p.price));
                if (candle.poc) topProfiles.add(candle.poc);
                sortedProfiles = sortedProfiles.filter(p => topProfiles.has(p.price));
            }
            
            sortedProfiles.forEach((profile) => {
                const priceY = profile.price;
                const bidVol = Math.round(profile.sell_volume);
                const askVol = Math.round(profile.buy_volume);
                const totalVol = bidVol + askVol;
                const isPOC = candle.poc && Math.abs(priceY - candle.poc) < tickSize / 2;
                
                if (totalVol === 0) return;
                
                // Bar extends from CENTER to RIGHT
                const barWidthRatio = totalVol / maxVol;
                const barWidth = barWidthRatio * maxBarWidth;
                const barX1 = timestampSec;  // Start at center line
                const barX2 = timestampSec + barWidth;  // Extend to the right
                
                // Color based on delta: green for more buys, purple for more sells
                const delta = askVol - bidVol;
                let barColor;
                if (delta > 0) {
                    // More buying - green with better opacity
                    const intensity = Math.min(Math.abs(delta) / totalVol, 1);
                    barColor = `rgba(38, 166, 154, ${0.6 + intensity * 0.35})`;  // Teal green
                } else if (delta < 0) {
                    // More selling - purple/pink with better opacity
                    const intensity = Math.min(Math.abs(delta) / totalVol, 1);
                    barColor = `rgba(186, 104, 200, ${0.6 + intensity * 0.35})`;  // Purple
                } else {
                    barColor = "rgba(150, 150, 150, 0.6)";  // Neutral gray
                }
                
                // Create the horizontal bar - full tick height for visibility
                const borderColor = isPOC ? "#ffff00" : "#555555";
                const borderThickness = isPOC ? 2 : 1;
                
                const barBox = new BoxAnnotation({
                    x1: barX1,
                    y1: priceY,
                    x2: barX2,
                    y2: priceY + tickSize,  // Full tick height
                    fill: barColor,
                    stroke: borderColor,
                    strokeThickness: borderThickness,
                    annotationLayer: EAnnotationLayer.BelowChart
                });
                mainSurface.annotations.add(barBox);
                profileAnnotations.push(barBox);
                
                // Add volume text inside the bar (centered) if wide enough
                if (barWidth > candleWidthSec * 0.1) {
                    const volText = new TextAnnotation({
                        x1: barX1 + barWidth / 2,
                        y1: priceY + tickSize / 2,
                        text: formatVol(totalVol),
                        fontSize: fontSize,
                        fontFamily: "Arial",
                        fontWeight: "bold",
                        textColor: "#ffffff",
                        horizontalAnchorPoint: EHorizontalAnchorPoint.Center,
                        verticalAnchorPoint: EVerticalAnchorPoint.Center,
                        annotationLayer: EAnnotationLayer.AboveChart
                    });
                    mainSurface.annotations.add(volText);
                    profileAnnotations.push(volText);
                }
            });
        }
        
        // Add POC line annotation for this candle - extends RIGHT from center (like order flow bars)
        if (candle.poc && showPOC) {
            const barWidth = candleWidthSec * 0.45;  // Match order flow bar width
            const pocLine = new LineAnnotation({
                x1: timestampSec,  // Start at center
                y1: candle.poc,
                x2: timestampSec + barWidth,  // Extend right
                y2: candle.poc,
                stroke: COLORS.poc,
                strokeThickness: 2,
                annotationLayer: EAnnotationLayer.AboveChart
            });
            mainSurface.annotations.add(pocLine);
            profileAnnotations.push(pocLine);
        }
        
        // Add Value Area visualization - extends RIGHT from center (like order flow bars)
        if (candle.vah && candle.val && showVA) {
            const barWidth = candleWidthSec * 0.45;  // Match order flow bar width
            
            // Value Area shaded box (subtle fill) - right side only
            const vaBox = new BoxAnnotation({
                x1: timestampSec,  // Start at center
                y1: candle.val,
                x2: timestampSec + barWidth,  // Extend right
                y2: candle.vah,
                fill: "rgba(100, 100, 255, 0.1)",  // Subtle fill
                stroke: "transparent",
                annotationLayer: EAnnotationLayer.BelowChart
            });
            mainSurface.annotations.add(vaBox);
            profileAnnotations.push(vaBox);
            
            // VAH line (Value Area High) - green/teal, right side only
            const vahLine = new LineAnnotation({
                x1: timestampSec,  // Start at center
                y1: candle.vah,
                x2: timestampSec + barWidth,  // Extend right
                y2: candle.vah,
                stroke: "#26a69a",  // Teal green
                strokeThickness: 1,
                strokeDashArray: [4, 2],  // Dashed line
                annotationLayer: EAnnotationLayer.AboveChart
            });
            mainSurface.annotations.add(vahLine);
            profileAnnotations.push(vahLine);
            
            // VAL line (Value Area Low) - red/orange, right side only
            const valLine = new LineAnnotation({
                x1: timestampSec,  // Start at center
                y1: candle.val,
                x2: timestampSec + barWidth,  // Extend right
                y2: candle.val,
                stroke: "#ef5350",  // Red
                strokeThickness: 1,
                strokeDashArray: [4, 2],  // Dashed line
                annotationLayer: EAnnotationLayer.AboveChart
            });
            mainSurface.annotations.add(valLine);
            profileAnnotations.push(valLine);
        }
    });

    // Update candlestick series visibility
    const showCandles = document.getElementById('show-candles')?.classList.contains('active') ?? true;
    if (!showCandles) {
        candleSeries.opacity = 0;  // Hide candles completely
    } else if (showFootprints && !showOrderFlow) {
        candleSeries.opacity = 0.15;  // Dim candles for footprint view
    } else {
        candleSeries.opacity = 1.0;  // Full opacity otherwise
    }
    candleSeries.dataSeries.appendRange(xValues, openValues, highValues, lowValues, closeValues);
    
    // Update volume series
    volumeSeries.dataSeries.appendRange(xValues, volumeValues);
    
    // Update indicator series
    if (deltaSeries) {
        deltaSeries.dataSeries.appendRange(xValues, deltaValues);
    }
    if (cvdSeries) {
        cvdSeries.dataSeries.appendRange(xValues, cvdValues);
    }

    // Zoom to fit the data
    if (xValues.length > 0) {
        // Calculate proper ranges from data
        const xMin = Math.min(...xValues);
        const xMax = Math.max(...xValues);
        const yMin = Math.min(...lowValues);
        const yMax = Math.max(...highValues);
        
        // Add padding
        const xPadding = (xMax - xMin) * 0.05;
        const yPadding = (yMax - yMin) * 0.1;
        
        // Set visible ranges explicitly
        const xAxis = mainSurface.xAxes.get(0);
        const yAxis = mainSurface.yAxes.get(0);
        
        if (xAxis) {
            xAxis.visibleRange = new NumberRange(xMin - xPadding, xMax + xPadding);
        }
        if (yAxis) {
            yAxis.visibleRange = new NumberRange(yMin - yPadding, yMax + yPadding);
        }
        
        // Also sync indicator chart X axis
        if (indicatorSurface && indicatorSurface.xAxes.get(0)) {
            indicatorSurface.xAxes.get(0).visibleRange = new NumberRange(xMin - xPadding, xMax + xPadding);
        }
        
        console.log(`Zoomed to data: X=${new Date(xMin*1000).toISOString().slice(11,16)}-${new Date(xMax*1000).toISOString().slice(11,16)}, Y=$${yMin.toFixed(0)}-$${yMax.toFixed(0)}`);
    }
    
    // Render heatmap first (behind chart)
    renderHeatmap();
    
    // Render volume bubbles if enabled (above chart)
    renderBubbles();
    
    console.log("Chart rendered with", candles.length, "candles, timeframe:", timeframe);
}

function updateStats(data) {
    const { candles, timeframe } = data;
    
    if (!candles || candles.length === 0) return;
    
    let totalVol = 0;
    let totalDelta = 0;
    let highPrice = -Infinity;
    let lowPrice = Infinity;
    
    candles.forEach(c => {
        totalVol += c.volume;
        totalDelta += c.total_delta;
        if (c.high > highPrice) highPrice = c.high;
        if (c.low < lowPrice) lowPrice = c.low;
    });
    
    // Format volume (with USD support)
    let volStr;
    if (showVolumeInUSD && avgPrice > 0) {
        const volUSD = totalVol * avgPrice;
        volStr = volUSD >= 1_000_000 ? '$' + (volUSD / 1_000_000).toFixed(1) + 'M' :
                 volUSD >= 1_000 ? '$' + (volUSD / 1_000).toFixed(0) + 'K' :
                 '$' + Math.round(volUSD);
    } else {
        volStr = totalVol > 1000 ? (totalVol / 1000).toFixed(1) + 'K' : totalVol.toFixed(2);
    }
    
    // Stats elements may not exist in current UI
    const statVol = document.getElementById('stat-vol');
    if (statVol) statVol.textContent = volStr;
    
    // Format delta with color
    const deltaEl = document.getElementById('stat-delta');
    if (deltaEl) {
        deltaEl.textContent = totalDelta.toFixed(2);
        deltaEl.className = 'stat-val ' + (totalDelta >= 0 ? 'positive' : 'negative');
    }
    
    // Candle count
    const statCandles = document.getElementById('stat-candles');
    if (statCandles) statCandles.textContent = candles.length;
    
    // Date range
    const startDate = new Date(candles[0].timestamp);
    const endDate = new Date(candles[candles.length - 1].timestamp);
    
    const formatDate = (d) => {
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) + 
               ' ' + d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false });
    };
    
    const statStart = document.getElementById('stat-start');
    const statEnd = document.getElementById('stat-end');
    if (statStart) statStart.textContent = formatDate(startDate);
    if (statEnd) statEnd.textContent = formatDate(endDate);
    
    // Price range
    const statHigh = document.getElementById('stat-high');
    const statLow = document.getElementById('stat-low');
    if (statHigh) statHigh.textContent = '$' + highPrice.toLocaleString();
    if (statLow) statLow.textContent = '$' + lowPrice.toLocaleString();
}

/**
 * Load volume bubbles (large trades) for the current time range
 */
async function loadBubbles(candles) {
    if (!candles || candles.length === 0) return;
    
    const startTs = candles[0].timestamp;
    const endTs = candles[candles.length - 1].timestamp;
    
    // Get size thresholds from sliders (values are in $K)
    const minSlider = document.getElementById('bubble-min-slider');
    const maxSlider = document.getElementById('bubble-max-slider');
    const minSizeUsd = (parseInt(minSlider?.value) || 100) * 1000;  // Convert $K to $
    const maxSizeUsd = (parseInt(maxSlider?.value) || 5000) * 1000;
    
    const url = `/api/heatmap/bubbles?start_ts=${startTs}&end_ts=${endTs}&min_size_usd=${minSizeUsd}&max_size_usd=${maxSizeUsd}&limit=1000`;
    
    try {
        console.log(`Loading bubbles: ${url}`);
        const resp = await fetch(url);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        
        const data = await resp.json();
        bubbleData = data.bubbles || [];
        console.log(`Loaded ${bubbleData.length} volume bubbles`);
    } catch (err) {
        console.error("Failed to load bubbles:", err);
        bubbleData = [];
    }
}

/**
 * Render volume bubbles as circle annotations
 */
function renderBubbles() {
    // Clear existing bubble annotations
    bubbleAnnotations.forEach(ann => {
        try { mainSurface.annotations.remove(ann); } catch(e) {}
    });
    bubbleAnnotations = [];
    
    const showBubbles = document.getElementById('show-bubbles')?.classList.contains('active') ?? false;
    if (!showBubbles || !bubbleData || bubbleData.length === 0) return;
    
    // Find max volume for scaling
    const maxVol = Math.max(...bubbleData.map(b => b.quote_qty));
    const minRadius = 5;
    const maxRadius = 25;
    
    bubbleData.forEach(bubble => {
        const timestampSec = bubble.timestamp_ms / 1000;
        const price = bubble.price;
        const volume = bubble.quote_qty;
        
        // Scale radius based on volume (sqrt for better visual scaling)
        const volRatio = Math.sqrt(volume / maxVol);
        const radius = minRadius + volRatio * (maxRadius - minRadius);
        
        // Color based on buy/sell
        const color = bubble.is_buy 
            ? 'rgba(38, 166, 154, 0.7)'   // Green for buy
            : 'rgba(239, 83, 80, 0.7)';    // Red for sell
        const borderColor = bubble.is_buy ? '#26a69a' : '#ef5350';
        
        // Create SVG circle for the bubble
        const svgString = `
            <svg width="${radius * 2 + 4}" height="${radius * 2 + 4}">
                <circle cx="${radius + 2}" cy="${radius + 2}" r="${radius}" 
                    fill="${color}" stroke="${borderColor}" stroke-width="1.5"/>
            </svg>
        `;
        
        const annotation = new CustomAnnotation({
            x1: timestampSec,
            y1: price,
            horizontalAnchorPoint: EHorizontalAnchorPoint.Center,
            verticalAnchorPoint: EVerticalAnchorPoint.Center,
            svgString: svgString,
            annotationLayer: EAnnotationLayer.AboveChart
        });
        
        mainSurface.annotations.add(annotation);
        bubbleAnnotations.push(annotation);
    });
    
    console.log(`Rendered ${bubbleAnnotations.length} bubbles`);
}

/**
 * Load liquidity heatmap data (order book depth) for the current time range.
 * 
 * For a proper heatmap visualization:
 * - Uses FINE time granularity (5-10 seconds) to create continuous horizontal bands
 * - Fetches data for the ENTIRE visible price range
 * - Each time slice shows the order book state at that moment
 * - Large orders appear as bright horizontal lines that persist over time
 */
async function loadHeatmap(candles) {
    if (!candles || candles.length === 0) return;
    
    const startTs = candles[0].timestamp;
    const endTs = candles[candles.length - 1].timestamp;
    const exchange = document.getElementById('exchange-select')?.value || 'binance';
    
    // Get visible price range from chart
    let priceMin = null, priceMax = null;
    if (mainSurface) {
        const yAxis = mainSurface.yAxes.get(0);
        if (yAxis && yAxis.visibleRange) {
            priceMin = Math.floor(yAxis.visibleRange.min);
            priceMax = Math.ceil(yAxis.visibleRange.max);
        }
    }
    
    let url;
    if (exchange === 'bybit') {
        // Use FINE time granularity (5 seconds) for continuous horizontal bands
        // This creates the "trail" effect where orders persist across time
        const timeBucketSec = 5;  // 5-second slices for fine resolution
        const priceBucket = 1;    // $1 price buckets
        
        // IMPORTANT: Do NOT filter by price range here - load ALL data for the time range
        // The canvas renderer will handle visibility filtering
        // This ensures we have complete order book data regardless of zoom level
        url = `/api/heatmap/bybit/depth?start_ts=${startTs}&end_ts=${endTs}&price_bucket=${priceBucket}&time_bucket_sec=${timeBucketSec}`;
    } else {
        // Use Binance depth endpoint
        const maxSnapshots = Math.min(candles.length * 2, 500);
        url = `/api/heatmap/depth?start_ts=${startTs}&end_ts=${endTs}&max_snapshots=${maxSnapshots}`;
    }
    
    try {
        console.log(`Loading heatmap: ${url}`);
        const resp = await fetch(url);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        
        const data = await resp.json();
        
        if (exchange === 'bybit') {
            // Store with time bucket info for proper rendering
            heatmapData = {
                exchange: 'bybit',
                data: data.data || [],
                timeBucketSec: data.time_bucket_sec || 5,
                priceBucket: data.price_bucket || 1,
                candles: candles
            };
            console.log(`Loaded ${heatmapData.data.length} Bybit depth data points (${data.time_bucket_sec}s buckets)`);
        } else {
            heatmapData = {
                exchange: 'binance',
                snapshots: data.snapshots || [],
                candles: candles
            };
            console.log(`Loaded ${heatmapData.snapshots.length} depth snapshots`);
        }
    } catch (err) {
        console.error("Failed to load heatmap:", err);
        heatmapData = null;
    }
}

/**
 * Render liquidity heatmap - supports both historical and live data
 */
function renderHeatmap() {
    // Clear existing heatmap (annotations, series, AND canvas)
    heatmapAnnotations.forEach(ann => {
        try { mainSurface.annotations.remove(ann); } catch(e) {}
    });
    heatmapAnnotations = [];
    
    if (heatmapSeries) {
        try { mainSurface.renderableSeries.remove(heatmapSeries); } catch(e) {}
        heatmapSeries = null;
    }
    
    // Clear the canvas overlay
    const canvas = document.getElementById('heatmap-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
    
    const showHeatmap = document.getElementById('show-heatmap')?.classList.contains('active') ?? false;
    if (!showHeatmap) return;
    
    // Check for Bybit historical data first
    if (heatmapData && heatmapData.exchange === 'bybit' && heatmapData.data?.length > 0) {
        console.log(`Rendering Bybit historical heatmap with ${heatmapData.data.length} data points`);
        renderBybitHistoricalHeatmap(heatmapData.data);
        return;
    }
    
    // Check if we have live order book data
    if (window.liveOrderBook && window.liveOrderBook.length) {
        renderLiveHeatmap(window.liveOrderBook);
        return;
    }
    
    console.log("Heatmap: No data available (enable 'Heatmap' toggle and reload)");
}

/**
 * Canvas-based heatmap rendering for Bybit historical order book data.
 * 
 * CANVAS APPROACH - DATA-DRIVEN:
 * - Iterates through ORDER BOOK DATA and draws each point
 * - Each data point is a (timestamp, price, size, side) that gets mapped to canvas coordinates
 * - This ensures ALL available data is rendered, not just what matches pixel positions
 * - Creates horizontal bands where liquidity persists over time
 * - Bids = blue/cyan, Asks = orange/yellow
 */
function renderBybitHistoricalHeatmap(data) {
    if (!data || data.length === 0) return;
    if (!mainSurface) return;
    
    // Get canvas and context
    const canvas = document.getElementById('heatmap-canvas');
    if (!canvas) {
        console.error("Heatmap canvas not found");
        return;
    }
    
    // Get the SciChart container dimensions
    const chartDiv = document.getElementById('sci-chart-div');
    if (!chartDiv) return;
    
    const rect = chartDiv.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;
    canvas.style.width = rect.width + 'px';
    canvas.style.height = rect.height + 'px';
    
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Get visible ranges from SciChart axes
    const xAxis = mainSurface.xAxes.get(0);
    const yAxis = mainSurface.yAxes.get(0);
    if (!xAxis || !yAxis) return;
    
    const xMinSec = xAxis.visibleRange.min;  // Seconds
    const xMaxSec = xAxis.visibleRange.max;
    const yMin = yAxis.visibleRange.min;  // Price
    const yMax = yAxis.visibleRange.max;
    
    // Chart plot area (accounting for axis labels)
    const padding = { left: 0, right: 60, top: 10, bottom: 30 };
    const plotWidth = canvas.width - padding.left - padding.right;
    const plotHeight = canvas.height - padding.top - padding.bottom;
    
    // Get opacity from slider
    const opacitySlider = document.getElementById('heatmap-opacity');
    const opacity = (parseInt(opacitySlider?.value) || 40) / 100;
    
    // Convert axis range to milliseconds for data matching
    const xMinMs = xMinSec * 1000;
    const xMaxMs = xMaxSec * 1000;
    const xRangeMs = xMaxMs - xMinMs;
    const yRange = yMax - yMin;
    
    // Calculate pixel sizes for data points
    const timeBucketSec = heatmapData?.timeBucketSec || 5;
    const priceBucket = heatmapData?.priceBucket || 1;
    
    // Width of each time bucket in pixels
    const bucketWidthPx = Math.max(1, (timeBucketSec * 1000 / xRangeMs) * plotWidth);
    // Height of each price bucket in pixels
    const bucketHeightPx = Math.max(1, (priceBucket / yRange) * plotHeight);
    
    // Normalization: use 80th percentile for better color distribution
    const sizes = data.map(d => d.size).filter(s => s > 0).sort((a, b) => a - b);
    const normMax = sizes[Math.floor(sizes.length * 0.8)] || 1;
    
    console.log(`Canvas heatmap: ${plotWidth}x${plotHeight}px, ` +
                `time ${new Date(xMinMs).toLocaleTimeString()}-${new Date(xMaxMs).toLocaleTimeString()}, ` +
                `prices $${yMin.toFixed(0)}-$${yMax.toFixed(0)}, ` +
                `${data.length} data points, bucket ${bucketWidthPx.toFixed(1)}x${bucketHeightPx.toFixed(1)}px`);
    
    // DATA-DRIVEN RENDERING: iterate through each data point and draw it
    let rendered = 0;
    let skippedOutOfRange = 0;
    
    data.forEach(d => {
        const { timestamp, price, size, side } = d;
        
        // Skip if outside visible range
        if (timestamp < xMinMs || timestamp > xMaxMs) {
            skippedOutOfRange++;
            return;
        }
        if (price < yMin || price > yMax) {
            skippedOutOfRange++;
            return;
        }
        if (size <= 0) return;
        
        // Map data coordinates to canvas pixels
        const px = padding.left + ((timestamp - xMinMs) / xRangeMs) * plotWidth;
        const py = padding.top + ((yMax - price) / yRange) * plotHeight;
        
        // Calculate color intensity based on size
        const intensity = Math.min(size / normMax, 1.5);  // Allow slight overshoot for bright colors
        const alpha = opacity * Math.pow(Math.min(intensity, 1.0), 0.4);  // Gamma correction
        
        // Choose color based on side
        let r, g, b;
        if (side === 'bid') {
            // Cyan/Blue for bids - brighter for larger orders
            r = Math.floor(0 + intensity * 80);
            g = Math.floor(120 + intensity * 135);
            b = Math.floor(180 + intensity * 75);
        } else {
            // Orange/Yellow for asks - brighter for larger orders
            r = Math.floor(220 + intensity * 35);
            g = Math.floor(140 + intensity * 115);
            b = Math.floor(0 + intensity * 60);
        }
        
        // Draw a rectangle for this data point
        ctx.fillStyle = `rgba(${Math.min(r, 255)}, ${Math.min(g, 255)}, ${Math.min(b, 255)}, ${alpha})`;
        ctx.fillRect(
            Math.floor(px), 
            Math.floor(py - bucketHeightPx/2), 
            Math.ceil(bucketWidthPx), 
            Math.ceil(bucketHeightPx)
        );
        rendered++;
    });
    
    console.log(`Canvas heatmap: Rendered ${rendered} rectangles (${skippedOutOfRange} outside range)`);
}

/**
 * Fallback renderer using BoxAnnotations when grid is too large.
 */
function renderBybitHistoricalHeatmapFallback(data) {
    const timeBucketSec = heatmapData?.timeBucketSec || 5;
    const priceBucket = heatmapData?.priceBucket || 1;
    
    const opacitySlider = document.getElementById('heatmap-opacity');
    const opacityMultiplier = (parseInt(opacitySlider?.value) || 40) / 100;
    
    const sizes = data.map(d => d.size).filter(s => s > 0).sort((a, b) => a - b);
    const p95 = sizes[Math.floor(sizes.length * 0.95)] || 1;
    
    let rendered = 0;
    data.forEach(d => {
        const { timestamp, side, price, size } = d;
        const timeSec = timestamp / 1000;
        const normalizedSize = Math.min(size / p95, 2.0);
        const intensity = Math.pow(normalizedSize, 0.5);
        const alpha = Math.min(0.1 + intensity * 0.6, 0.9) * opacityMultiplier;
        
        let color;
        if (side === 'bid') {
            const r = Math.floor(0 + intensity * 100);
            const g = Math.floor(80 + intensity * 175);
            const b = Math.floor(120 + intensity * 135);
            color = `rgba(${Math.min(r, 255)}, ${Math.min(g, 255)}, ${Math.min(b, 255)}, ${alpha})`;
        } else {
            const r = Math.floor(180 + intensity * 75);
            const g = Math.floor(80 + intensity * 175);
            const b = Math.floor(0 + intensity * 80);
            color = `rgba(${Math.min(r, 255)}, ${Math.min(g, 255)}, ${Math.min(b, 255)}, ${alpha})`;
        }
        
        try {
            const annotation = new SciChart.BoxAnnotation({
                x1: timeSec, x2: timeSec + timeBucketSec,
                y1: price, y2: price + priceBucket,
                fill: color, stroke: 'transparent', strokeThickness: 0
            });
            mainSurface.annotations.add(annotation);
            heatmapAnnotations.push(annotation);
            rendered++;
        } catch (e) {}
    });
    
    console.log(`Heatmap fallback: Rendered ${rendered} boxes`);
}

/**
 * Render heatmap from live order book snapshots
 * @param {Array} orderBookSnapshots - Array of {timestamp, bids: [[price, qty], ...], asks: [[price, qty], ...]}
 */
function renderLiveHeatmap(orderBookSnapshots) {
    if (!orderBookSnapshots || orderBookSnapshots.length === 0) return;
    if (!mainSurface) return;
    
    // Get opacity from slider
    const opacitySlider = document.getElementById('heatmap-opacity');
    const baseOpacity = (parseInt(opacitySlider?.value) || 40) / 100;
    
    // Get visible Y range from chart
    const yAxis = mainSurface.yAxes.get(0);
    if (!yAxis) return;
    
    const visibleMin = yAxis.visibleRange.min;
    const visibleMax = yAxis.visibleRange.max;
    const priceRange = visibleMax - visibleMin;
    
    // Dynamic bucket size based on price range
    // At $500 range, use $5 buckets; at $5000 range, use $50 buckets
    const bucketSize = Math.max(1, Math.round(priceRange / 100));
    
    // Aggregate orders into price buckets for cleaner visualization
    // Group snapshots by time periods too (e.g., 30 second windows)
    const timeframeMins = parseInt(document.getElementById('tf-select')?.value) || 5;
    const timeWindow = timeframeMins * 60 * 1000; // Match candle width
    
    // Group snapshots by time window and aggregate quantities at price buckets
    const aggregated = new Map(); // Map<timeWindow, Map<priceBucket, {bidQty, askQty}>>
    
    orderBookSnapshots.forEach(snap => {
        const windowStart = Math.floor(snap.timestamp / timeWindow) * timeWindow;
        
        if (!aggregated.has(windowStart)) {
            aggregated.set(windowStart, new Map());
        }
        const buckets = aggregated.get(windowStart);
        
        // Process bids
        snap.bids.forEach(([price, qty]) => {
            if (price < visibleMin || price > visibleMax) return;
            const bucket = Math.floor(price / bucketSize) * bucketSize;
            if (!buckets.has(bucket)) {
                buckets.set(bucket, { bidQty: 0, askQty: 0, count: 0 });
            }
            const b = buckets.get(bucket);
            b.bidQty = Math.max(b.bidQty, qty); // Use max to show peak liquidity
            b.count++;
        });
        
        // Process asks
        snap.asks.forEach(([price, qty]) => {
            if (price < visibleMin || price > visibleMax) return;
            const bucket = Math.floor(price / bucketSize) * bucketSize;
            if (!buckets.has(bucket)) {
                buckets.set(bucket, { bidQty: 0, askQty: 0, count: 0 });
            }
            const b = buckets.get(bucket);
            b.askQty = Math.max(b.askQty, qty);
            b.count++;
        });
    });
    
    // Find max quantity for normalization
    let maxQty = 0;
    aggregated.forEach(buckets => {
        buckets.forEach(data => {
            if (data.bidQty > maxQty) maxQty = data.bidQty;
            if (data.askQty > maxQty) maxQty = data.askQty;
        });
    });
    
    if (maxQty === 0) return;
    
    // Render aggregated buckets
    aggregated.forEach((buckets, windowStart) => {
        const x1 = windowStart / 1000;
        const x2 = (windowStart + timeWindow) / 1000;
        
        buckets.forEach((data, priceBucket) => {
            // Render bid if present
            if (data.bidQty > 0) {
                const intensity = Math.pow(data.bidQty / maxQty, 0.5); // Square root for better distribution
                const opacity = baseOpacity * (0.15 + 0.85 * intensity);
                
                const annotation = new BoxAnnotation({
                    x1: x1,
                    y1: priceBucket,
                    x2: x2,
                    y2: priceBucket + bucketSize,
                    fill: `rgba(38, 166, 154, ${opacity.toFixed(2)})`,
                    stroke: 'transparent',
                    annotationLayer: EAnnotationLayer.BelowChart
                });
                
                mainSurface.annotations.add(annotation);
                heatmapAnnotations.push(annotation);
            }
            
            // Render ask if present
            if (data.askQty > 0) {
                const intensity = Math.pow(data.askQty / maxQty, 0.5);
                const opacity = baseOpacity * (0.15 + 0.85 * intensity);
                
                const annotation = new BoxAnnotation({
                    x1: x1,
                    y1: priceBucket,
                    x2: x2,
                    y2: priceBucket + bucketSize,
                    fill: `rgba(239, 83, 80, ${opacity.toFixed(2)})`,
                    stroke: 'transparent',
                    annotationLayer: EAnnotationLayer.BelowChart
                });
                
                mainSurface.annotations.add(annotation);
                heatmapAnnotations.push(annotation);
            }
        });
    });
    
    console.log(`Rendered ${heatmapAnnotations.length} live heatmap bands (${aggregated.size} windows)`);
}

function setIndicatorMode(mode) {
    indicatorMode = mode;
    
    // Update visibility
    if (deltaSeries) {
        deltaSeries.isVisible = (mode === 'delta');
    }
    if (cvdSeries) {
        cvdSeries.isVisible = (mode === 'cvd' || mode === 'cvd_line');
    }
    
    // Update axis title
    const yAxis = indicatorSurface?.yAxes.get(0);
    if (yAxis) {
        yAxis.axisTitle = mode === 'delta' ? 'Delta' : 'CVD';
    }
    
    // Update button states
    document.querySelectorAll('.indicator-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });
    
    console.log("Indicator mode:", mode);
}

// Init
document.addEventListener('DOMContentLoaded', async () => {
    document.getElementById('loading').style.display = 'flex';
    
    // DON'T set date input - leave empty so API returns LATEST available data
    // If user wants a specific date, they can enter it manually and click Go
    const initDateEl = document.getElementById('start-date');
    const initTimeEl = document.getElementById('start-time-clock');
    if (initDateEl) {
        initDateEl.value = '';  // Empty = load latest data
        if (initTimeEl) {
            initTimeEl.value = '00:00';
        }
    }
    
    const success = await initSciChart();
    if (success) {
        await initIndicatorChart();
        
        // Auto-load data on start
        await loadData();
    }
    
    // Event listeners
    document.getElementById('load-btn').addEventListener('click', loadData);
    
    // Timeframe change
    document.getElementById('tf-select').addEventListener('change', () => {
        console.log("Timeframe changed to:", document.getElementById('tf-select').value);
        loadData();
    });
    
    // DOM aggregation change - refresh order book display
    document.getElementById('dom-aggregation')?.addEventListener('change', () => {
        if (historicalOrderBook) {
            updateDOMHistorical(historicalOrderBook);
        }
    });
    
    // Tick size change (debounced) - mark as user-set
    let tickTimeout;
    document.getElementById('tick-size').addEventListener('input', (e) => {
        e.target.dataset.userSet = 'true';  // User manually changed, don't auto-adjust
        clearTimeout(tickTimeout);
        tickTimeout = setTimeout(loadData, 500);
    });
    
    // Reset user-set flag when timeframe changes
    document.getElementById('tf-select').addEventListener('change', () => {
        document.getElementById('tick-size').dataset.userSet = '';  // Allow auto-adjust
    }, { capture: true });
    
    // Candle limit change (debounced)
    let limitTimeout;
    document.getElementById('candle-limit').addEventListener('input', () => {
        clearTimeout(limitTimeout);
        limitTimeout = setTimeout(loadData, 500);
    });
    
    // Indicator mode buttons
    document.querySelectorAll('.indicator-btn').forEach(btn => {
        btn.addEventListener('click', () => setIndicatorMode(btn.dataset.mode));
    });
    
    // Toggle buttons - re-render with current data
    // Footprint and Order Flow are mutually exclusive
    const footprintBtn = document.getElementById('show-footprint');
    const orderflowBtn = document.getElementById('show-orderflow');
    
    footprintBtn?.addEventListener('click', () => {
        footprintBtn.classList.toggle('active');
        // If activating footprint, deactivate orderflow
        if (footprintBtn.classList.contains('active') && orderflowBtn) {
            orderflowBtn.classList.remove('active');
        }
        if (currentData) renderData(currentData);
    });
    
    orderflowBtn?.addEventListener('click', () => {
        orderflowBtn.classList.toggle('active');
        // If activating orderflow, deactivate footprint
        if (orderflowBtn.classList.contains('active') && footprintBtn) {
            footprintBtn.classList.remove('active');
        }
        if (currentData) renderData(currentData);
    });
    
    // POC, VA, and Candles are independent toggles
    ['show-poc', 'show-va', 'show-candles'].forEach(id => {
        document.getElementById(id)?.addEventListener('click', (e) => {
            e.target.classList.toggle('active');
            if (currentData) renderData(currentData);
        });
    });
    
    // Bubbles toggle - loads/shows volume bubbles (large trades)
    const bubblesBtn = document.getElementById('show-bubbles');
    const bubbleSliderGroup = document.getElementById('bubble-slider-group');
    const bubbleMinSlider = document.getElementById('bubble-min-slider');
    const bubbleMaxSlider = document.getElementById('bubble-max-slider');
    const bubbleValueDisplay = document.getElementById('bubble-value-display');
    const bubbleSliderRange = document.getElementById('bubble-slider-range');
    
    // Format value for display (e.g., 100 -> "100K", 1000 -> "1M")
    function formatBubbleValue(val) {
        if (val >= 1000) return (val / 1000).toFixed(1).replace('.0', '') + 'M';
        return val + 'K';
    }
    
    // Update the slider range highlight and display
    function updateBubbleSliderUI() {
        const min = parseInt(bubbleMinSlider.value);
        const max = parseInt(bubbleMaxSlider.value);
        const rangeMin = parseInt(bubbleMinSlider.min);
        const rangeMax = parseInt(bubbleMinSlider.max);
        
        // Calculate percentages for positioning
        const minPercent = ((min - rangeMin) / (rangeMax - rangeMin)) * 100;
        const maxPercent = ((max - rangeMin) / (rangeMax - rangeMin)) * 100;
        
        // Update the highlighted range
        bubbleSliderRange.style.left = minPercent + '%';
        bubbleSliderRange.style.width = (maxPercent - minPercent) + '%';
        
        // Update display text
        bubbleValueDisplay.textContent = formatBubbleValue(min) + ' - ' + formatBubbleValue(max);
    }
    
    // Slider event handlers
    let bubbleSliderTimeout;
    function onBubbleSliderChange() {
        // Ensure min doesn't exceed max and vice versa
        const min = parseInt(bubbleMinSlider.value);
        const max = parseInt(bubbleMaxSlider.value);
        
        if (min > max) {
            bubbleMinSlider.value = max;
        }
        if (max < min) {
            bubbleMaxSlider.value = min;
        }
        
        updateBubbleSliderUI();
        
        // Debounce the data reload
        clearTimeout(bubbleSliderTimeout);
        bubbleSliderTimeout = setTimeout(async () => {
            if (currentData && currentData.candles?.length > 0) {
                await loadBubbles(currentData.candles);
                renderBubbles();
            }
        }, 300);
    }
    
    bubbleMinSlider?.addEventListener('input', onBubbleSliderChange);
    bubbleMaxSlider?.addEventListener('input', onBubbleSliderChange);
    
    // Initialize slider UI
    updateBubbleSliderUI();
    
    if (bubblesBtn) {
        bubblesBtn.addEventListener('click', async () => {
            bubblesBtn.classList.toggle('active');
            const isActive = bubblesBtn.classList.contains('active');
            
            // Show/hide the slider group
            bubbleSliderGroup?.classList.toggle('visible', isActive);
            
            if (isActive) {
                // Load bubbles if we have candle data for time range
                if (currentData && currentData.candles?.length > 0) {
                    await loadBubbles(currentData.candles);
                }
            }
            renderBubbles();
        });
    }
    
    // Heatmap toggle - shows HISTORICAL liquidity depth (NOT live WebSocket)
    const heatmapBtn = document.getElementById('show-heatmap');
    const heatmapControls = document.getElementById('heatmap-controls');
    const heatmapOpacitySlider = document.getElementById('heatmap-opacity');
    const heatmapOpacityDisplay = document.getElementById('heatmap-opacity-display');
    
    // Opacity slider handler
    heatmapOpacitySlider?.addEventListener('input', () => {
        const val = heatmapOpacitySlider.value;
        heatmapOpacityDisplay.textContent = val + '%';
        renderHeatmap();  // Re-render with new opacity
    });
    
    if (heatmapBtn) {
        heatmapBtn.addEventListener('click', async () => {
            heatmapBtn.classList.toggle('active');
            const isActive = heatmapBtn.classList.contains('active');
            
            // Show/hide the controls
            heatmapControls?.classList.toggle('visible', isActive);
            
            if (isActive) {
                // Load HISTORICAL heatmap data (NOT live WebSocket)
                if (currentData && currentData.candles?.length > 0) {
                    updateHeatmapStatus("Loading historical...");
                    await loadHeatmap(currentData.candles);
                    const count = heatmapData?.data?.length || heatmapData?.snapshots?.length || 0;
                    updateHeatmapStatus(`Historical: ${count} points`);
                } else {
                    updateHeatmapStatus("No candle data");
                }
            } else {
                updateHeatmapStatus("Off");
            }
            renderHeatmap();
        });
    }
    
    // Record button - controls recording independently
    const recordBtn = document.getElementById('record-btn');
    if (recordBtn) {
        recordBtn.addEventListener('click', async () => {
            if (isRecording) {
                await stopRecording();
            } else {
                await startRecording();
            }
        });
    }
    
    // USD/BTC toggle button
    const volToggle = document.getElementById('vol-unit-toggle');
    if (volToggle) {
        // Set initial state
        volToggle.classList.toggle('active', showVolumeInUSD);
        volToggle.textContent = showVolumeInUSD ? 'USD' : 'BTC';
        
        volToggle.addEventListener('click', () => {
            showVolumeInUSD = !showVolumeInUSD;
            volToggle.classList.toggle('active', showVolumeInUSD);
            volToggle.textContent = showVolumeInUSD ? 'USD' : 'BTC';
            if (currentData) {
                renderData(currentData);
                updateStats(currentData);
            }
        });
    }
    
    // Date/Time picker - separate inputs for visual selection
    const startDateEl = document.getElementById('start-date');
    const startTimeClockEl = document.getElementById('start-time-clock');
    const goBtn = document.getElementById('go-to-date');
    
    // Go button loads data from the selected date/time
    if (goBtn) {
        goBtn.addEventListener('click', () => {
            const dateVal = startDateEl?.value;
            const timeVal = startTimeClockEl?.value || '00:00';
            if (dateVal) {
                console.log(`Go button: Loading ${dateVal} ${timeVal}`);
                loadData();
            } else {
                console.log("Go button: No date selected, loading latest data");
                loadData();
            }
        });
    }
    
    // AutoScale Y-axis toggle
    const autoscaleBtn = document.getElementById('autoscale-toggle');
    if (autoscaleBtn && mainSurface) {
        autoscaleBtn.addEventListener('click', () => {
            autoscaleBtn.classList.toggle('active');
            const isAutoScale = autoscaleBtn.classList.contains('active');
            
            // Get the Y-axis and toggle autoRange
            const yAxis = mainSurface.yAxes.get(0);
            if (yAxis) {
                if (isAutoScale) {
                    yAxis.autoRange = EAutoRange.Always;
                } else {
                    yAxis.autoRange = EAutoRange.Never;
                }
            }
            console.log("AutoScale Y:", isAutoScale);
        });
    }
});
