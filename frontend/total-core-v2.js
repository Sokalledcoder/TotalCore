/**
 * Total Core V2 - Volume Profile / Footprint Chart
 * Uses Lightweight Charts (TradingView) for Canvas 2D rendering
 * No WebGL required - works on all browsers
 */

// ============================================================================
// State
// ============================================================================
let mainChart = null;
let indicatorChart = null;
let candleSeries = null;
let volumeSeries = null;
let deltaSeries = null;
let cvdSeries = null;
let currentData = null;
let indicatorMode = 'delta';

// Visualization toggles
let showCandles = true;
let showFootprint = true;
let showPOC = true;
let showVA = false;
let showBubbles = false;
let showHeatmap = false;
let showOrderFlow = false;
let autoScaleY = true;
let volumeInUSD = true;

// Live streaming
let isRecording = false;
let orderbookWebSocket = null;
let currentOrderBook = { bids: [], asks: [] };

// ============================================================================
// Chart Colors (matching TotalCore theme)
// ============================================================================
const COLORS = {
    background: '#000000',
    text: '#888888',
    textLight: '#e0e0e0',
    grid: '#1a1a1a',
    border: '#333333',
    
    upColor: '#26a69a',
    downColor: '#ef5350',
    
    poc: '#ffd700',
    vah: '#4caf50',
    val: '#f44336',
    
    delta: '#50C7E0',
    cvd: '#50C7E0',
    
    volumeUp: '#26a69a88',
    volumeDown: '#ef535088',
};

// ============================================================================
// Chart Initialization
// ============================================================================
async function initCharts() {
    try {
        updateLoadingText('Initializing charts...');
        
        // Main chart
        const mainContainer = document.getElementById('main-chart');
        mainChart = LightweightCharts.createChart(mainContainer, {
            layout: {
                background: { type: 'solid', color: COLORS.background },
                textColor: COLORS.text,
            },
            grid: {
                vertLines: { color: COLORS.grid },
                horzLines: { color: COLORS.grid },
            },
            crosshair: {
                mode: LightweightCharts.CrosshairMode.Normal,
                vertLine: {
                    color: '#ffffff44',
                    width: 1,
                    style: LightweightCharts.LineStyle.Solid,
                    labelBackgroundColor: '#000000cc',
                },
                horzLine: {
                    color: '#ffffff44',
                    width: 1,
                    style: LightweightCharts.LineStyle.Solid,
                    labelBackgroundColor: '#000000cc',
                },
            },
            rightPriceScale: {
                borderColor: COLORS.border,
                scaleMargins: { top: 0.1, bottom: 0.2 },
            },
            timeScale: {
                borderColor: COLORS.border,
                timeVisible: true,
                secondsVisible: false,
            },
            handleScale: {
                axisPressedMouseMove: { time: true, price: true },
            },
            handleScroll: {
                mouseWheel: true,
                pressedMouseMove: true,
            },
        });
        
        // Add candlestick series
        candleSeries = mainChart.addCandlestickSeries({
            upColor: COLORS.upColor,
            downColor: COLORS.downColor,
            borderVisible: false,
            wickUpColor: COLORS.upColor,
            wickDownColor: COLORS.downColor,
        });
        
        // Add volume series (histogram at bottom)
        volumeSeries = mainChart.addHistogramSeries({
            priceFormat: { type: 'volume' },
            priceScaleId: '', // Overlay on main chart
        });
        volumeSeries.priceScale().applyOptions({
            scaleMargins: { top: 0.85, bottom: 0 },
        });
        
        console.log('Main chart initialized');
        
        // Indicator chart
        const indicatorContainer = document.getElementById('indicator-chart');
        indicatorChart = LightweightCharts.createChart(indicatorContainer, {
            layout: {
                background: { type: 'solid', color: COLORS.background },
                textColor: COLORS.text,
            },
            grid: {
                vertLines: { color: COLORS.grid },
                horzLines: { color: COLORS.grid },
            },
            rightPriceScale: {
                borderColor: COLORS.border,
            },
            timeScale: {
                borderColor: COLORS.border,
                timeVisible: true,
                secondsVisible: false,
                visible: false, // Hide time scale on indicator (synced with main)
            },
            handleScale: { axisPressedMouseMove: false },
            handleScroll: { mouseWheel: false, pressedMouseMove: false },
        });
        
        // Delta histogram
        deltaSeries = indicatorChart.addHistogramSeries({
            color: COLORS.delta,
            priceFormat: { type: 'volume' },
        });
        
        // CVD line (hidden by default)
        cvdSeries = indicatorChart.addLineSeries({
            color: COLORS.cvd,
            lineWidth: 2,
            visible: false,
        });
        
        console.log('Indicator chart initialized');
        
        // Sync time scales
        mainChart.timeScale().subscribeVisibleLogicalRangeChange((range) => {
            if (range) {
                indicatorChart.timeScale().setVisibleLogicalRange(range);
            }
        });
        
        // Handle resize
        const resizeObserver = new ResizeObserver(() => {
            const mainRect = mainContainer.getBoundingClientRect();
            mainChart.applyOptions({ width: mainRect.width, height: mainRect.height });
            
            const indicatorRect = indicatorContainer.getBoundingClientRect();
            indicatorChart.applyOptions({ width: indicatorRect.width, height: indicatorRect.height });
            
            // Resize footprint canvas
            resizeFootprintCanvas();
        });
        resizeObserver.observe(mainContainer);
        resizeObserver.observe(indicatorContainer);
        
        return true;
    } catch (e) {
        console.error('Failed to initialize charts:', e);
        document.getElementById('loading').innerHTML = `
            <div style="color: #ff6b6b; text-align: center; padding: 20px;">
                <h3>Failed to initialize charts</h3>
                <p style="font-size: 12px; color: #888;">${e.message}</p>
            </div>
        `;
        return false;
    }
}

// ============================================================================
// Data Loading
// ============================================================================
async function loadData() {
    const symbol = document.getElementById('symbol-select').value;
    const exchange = document.getElementById('exchange-select').value;
    const timeframe = document.getElementById('tf-select').value;
    const limit = parseInt(document.getElementById('candle-limit').value) || 100;
    const tickSize = parseInt(document.getElementById('tick-size').value) || 1;
    
    // Build URL with optional date filter
    let url = `/api/footprint/candles?symbol=${symbol}&exchange=${exchange}&timeframe=${timeframe}&tick_size=${tickSize}&ticks_per_row=1&limit=${limit}`;
    
    const startDate = document.getElementById('start-date').value;
    const startTime = document.getElementById('start-time-clock').value;
    if (startDate) {
        const startMs = new Date(`${startDate}T${startTime || '00:00'}:00Z`).getTime();
        url += `&start_time=${startMs}`;
    }
    
    updateLoadingText(`Loading ${limit} candles...`);
    showLoading(true);
    
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        
        const data = await response.json();
        currentData = data;
        
        console.log(`Loaded ${data.candles?.length || 0} candles`);
        
        // Transform and set data
        setCandleData(data.candles || []);
        setIndicatorData(data.candles || []);
        
        // Draw footprint overlay
        if (showFootprint) {
            drawFootprint(data.candles || []);
        }
        
        // Fit content
        mainChart.timeScale().fitContent();
        
        showLoading(false);
    } catch (e) {
        console.error('Failed to load data:', e);
        showLoading(false);
        alert(`Failed to load data: ${e.message}`);
    }
}

function setCandleData(candles) {
    if (!candleSeries || !volumeSeries) return;
    
    // Transform to Lightweight Charts format
    // API returns timestamps in ms, LWC expects seconds
    const candleData = candles.map(c => ({
        time: Math.floor(c.timestamp / 1000),
        open: c.open,
        high: c.high,
        low: c.low,
        close: c.close,
    }));
    
    const volumeData = candles.map(c => ({
        time: Math.floor(c.timestamp / 1000),
        value: volumeInUSD ? (c.volume * c.close) : c.volume,
        color: c.close >= c.open ? COLORS.volumeUp : COLORS.volumeDown,
    }));
    
    candleSeries.setData(candleData);
    volumeSeries.setData(volumeData);
    
    // Toggle visibility
    candleSeries.applyOptions({ visible: showCandles });
}

function setIndicatorData(candles) {
    if (!deltaSeries || !cvdSeries) return;
    
    let cumulativeDelta = 0;
    const deltaData = [];
    const cvdData = [];
    
    candles.forEach(c => {
        const time = Math.floor(c.timestamp / 1000);
        // Use total_delta from API (already calculated)
        const delta = c.total_delta || 0;
        cumulativeDelta += delta;
        
        deltaData.push({
            time,
            value: delta,
            color: delta >= 0 ? COLORS.upColor : COLORS.downColor,
        });
        
        cvdData.push({
            time,
            value: cumulativeDelta,
        });
    });
    
    console.log(`Indicator data: ${deltaData.length} points, CVD range: ${cvdData[0]?.value} to ${cvdData[cvdData.length-1]?.value}`);
    
    deltaSeries.setData(deltaData);
    cvdSeries.setData(cvdData);
    
    // Set visibility based on mode
    deltaSeries.applyOptions({ visible: indicatorMode === 'delta' });
    cvdSeries.applyOptions({ visible: indicatorMode === 'cvd' });
}

// ============================================================================
// Footprint Drawing (Canvas Overlay)
// ============================================================================
function resizeFootprintCanvas() {
    const canvas = document.getElementById('footprint-canvas');
    const container = document.getElementById('chart-area');
    if (!canvas || !container) return;
    
    const rect = container.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;
    canvas.style.width = rect.width + 'px';
    canvas.style.height = rect.height + 'px';
    
    // Redraw if we have data
    if (currentData && showFootprint) {
        drawFootprint(currentData.candles || []);
    }
}

function drawFootprint(candles) {
    const canvas = document.getElementById('footprint-canvas');
    if (!canvas || !mainChart || !candleSeries) return;
    
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    if (!showFootprint || !candles.length) return;
    
    const timeScale = mainChart.timeScale();
    
    candles.forEach((candle, idx) => {
        // API returns 'profiles' not 'profile'
        const profiles = candle.profiles || candle.profile || [];
        if (!profiles.length) return;
        
        const time = Math.floor(candle.timestamp / 1000);
        const x = timeScale.timeToCoordinate(time);
        if (x === null) return;
        
        // Get candle width (approximate)
        const nextTime = idx < candles.length - 1 
            ? Math.floor(candles[idx + 1].timestamp / 1000) 
            : time + 60;
        const nextX = timeScale.timeToCoordinate(nextTime);
        const candleWidth = nextX !== null ? Math.abs(nextX - x) * 0.8 : 20;
        
        // Find max volume for normalization
        const maxVol = Math.max(...profiles.map(p => p.total_volume || 0), 1);
        
        // Draw each price level
        profiles.forEach(level => {
            const priceY = candleSeries.priceToCoordinate(level.price);
            if (priceY === null) return;
            
            const nextPriceY = candleSeries.priceToCoordinate(level.price + 1);
            const rowHeight = nextPriceY !== null ? Math.abs(nextPriceY - priceY) : 2;
            
            const volRatio = (level.total_volume || 0) / maxVol;
            const barWidth = candleWidth * volRatio;
            
            // Color by delta (use delta field directly from API)
            const delta = level.delta || 0;
            const alpha = 0.4 + (volRatio * 0.4);
            ctx.fillStyle = delta >= 0 
                ? `rgba(38, 166, 154, ${alpha})` 
                : `rgba(239, 83, 80, ${alpha})`;
            
            ctx.fillRect(x - barWidth / 2, priceY - rowHeight / 2, barWidth, Math.max(rowHeight, 1));
            
            // Draw POC marker
            if (showPOC && level.price === candle.poc) {
                ctx.fillStyle = COLORS.poc;
                ctx.fillRect(x - candleWidth / 2, priceY - 1, candleWidth, 2);
            }
        });
        
        // Draw VA lines if enabled
        if (showVA && candle.vah && candle.val) {
            ctx.strokeStyle = COLORS.vah;
            ctx.lineWidth = 1;
            const vahY = candleSeries.priceToCoordinate(candle.vah);
            if (vahY !== null) {
                ctx.beginPath();
                ctx.moveTo(x - candleWidth / 2, vahY);
                ctx.lineTo(x + candleWidth / 2, vahY);
                ctx.stroke();
            }
            
            ctx.strokeStyle = COLORS.val;
            const valY = candleSeries.priceToCoordinate(candle.val);
            if (valY !== null) {
                ctx.beginPath();
                ctx.moveTo(x - candleWidth / 2, valY);
                ctx.lineTo(x + candleWidth / 2, valY);
                ctx.stroke();
            }
        }
    });
}

// ============================================================================
// Order Book WebSocket & DOM Panel
// ============================================================================
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
        updateDOMStatus("Connected");
    };
    
    orderbookWebSocket.onmessage = (event) => {
        try {
            const msg = JSON.parse(event.data);
            
            if (msg.type === "snapshot" && msg.data) {
                currentOrderBook = {
                    bids: msg.data.bids || [],
                    asks: msg.data.asks || []
                };
                renderOrderBook();
            } else if (msg.type === "ping") {
                orderbookWebSocket.send(JSON.stringify({command: "pong"}));
            }
        } catch (e) {
            console.error("OrderBook WebSocket message error:", e);
        }
    };
    
    orderbookWebSocket.onerror = (error) => {
        console.error("OrderBook WebSocket error:", error);
        updateDOMStatus("Error");
    };
    
    orderbookWebSocket.onclose = () => {
        console.log("OrderBook WebSocket closed");
        updateDOMStatus("Disconnected");
        orderbookWebSocket = null;
    };
}

function disconnectOrderBookWebSocket() {
    if (orderbookWebSocket) {
        orderbookWebSocket.close();
        orderbookWebSocket = null;
    }
    currentOrderBook = { bids: [], asks: [] };
}

async function startOrderBookStreaming() {
    try {
        updateDOMStatus("Starting...");
        const exchange = document.getElementById('exchange-select')?.value || 'binance';
        const ccxtExchange = exchange === 'bybit' ? 'bybit' : 'binanceusdm';
        const symbol = 'BTC/USDT:USDT';
        // Bybit only accepts depth limits of [1, 50, 200, 1000] for swap markets
        const depthLimit = exchange === 'bybit' ? 200 : 500;
        
        const resp = await fetch(`/api/orderbook/start?exchange=${ccxtExchange}&symbol=${encodeURIComponent(symbol)}&depth_limit=${depthLimit}`, {method: 'POST'});
        const data = await resp.json();
        if (data.error) {
            updateDOMStatus(`Error: ${data.error}`);
        } else {
            console.log("Streaming started:", data);
            updateDOMStatus("Streaming");
            connectOrderBookWebSocket();
        }
    } catch (e) {
        console.error("Failed to start orderbook streaming:", e);
        updateDOMStatus("Failed");
    }
}

function updateDOMStatus(status) {
    const spread = document.getElementById('dom-spread');
    if (spread) spread.textContent = status;
}

function renderOrderBook() {
    const aggregation = parseFloat(document.getElementById('dom-aggregation')?.value || 5);
    const asksContainer = document.getElementById('dom-asks');
    const bidsContainer = document.getElementById('dom-bids');
    const midPriceEl = document.getElementById('dom-mid-price');
    
    if (!asksContainer || !bidsContainer) return;
    
    // Aggregate order book by price levels
    const aggregatedAsks = aggregateOrderBook(currentOrderBook.asks, aggregation);
    const aggregatedBids = aggregateOrderBook(currentOrderBook.bids, aggregation);
    
    // Find max quantity for bar width normalization
    const allQtys = [...aggregatedAsks.map(a => a.qty), ...aggregatedBids.map(b => b.qty)];
    const maxQty = Math.max(...allQtys, 1);
    
    // Calculate mid price and spread
    const bestBid = aggregatedBids[0]?.price || 0;
    const bestAsk = aggregatedAsks[0]?.price || 0;
    const spread = bestAsk > 0 && bestBid > 0 ? (bestAsk - bestBid).toFixed(2) : '-';
    const midPrice = bestAsk > 0 && bestBid > 0 ? ((bestAsk + bestBid) / 2).toFixed(2) : '-';
    
    if (midPriceEl) midPriceEl.textContent = midPrice;
    document.getElementById('dom-spread').textContent = `Spread: $${spread}`;
    
    // Render asks (reversed so lowest ask is at bottom)
    asksContainer.innerHTML = aggregatedAsks.slice(0, 15).reverse().map(level => {
        const barWidth = (level.qty / maxQty) * 100;
        return `<div class="dom-row">
            <div class="dom-qty">${level.qty.toFixed(3)}</div>
            <div class="dom-bar dom-bar-ask" style="width: ${barWidth}%"></div>
            <div class="dom-price dom-price-ask">${level.price.toFixed(1)}</div>
            <div class="dom-bar"></div>
            <div class="dom-qty"></div>
        </div>`;
    }).join('');
    
    // Render bids
    bidsContainer.innerHTML = aggregatedBids.slice(0, 15).map(level => {
        const barWidth = (level.qty / maxQty) * 100;
        return `<div class="dom-row">
            <div class="dom-qty"></div>
            <div class="dom-bar"></div>
            <div class="dom-price dom-price-bid">${level.price.toFixed(1)}</div>
            <div class="dom-bar dom-bar-bid" style="width: ${barWidth}%"></div>
            <div class="dom-qty">${level.qty.toFixed(3)}</div>
        </div>`;
    }).join('');
}

function aggregateOrderBook(levels, aggregation) {
    const aggregated = new Map();
    
    levels.forEach(([price, qty]) => {
        const roundedPrice = Math.floor(price / aggregation) * aggregation;
        const existing = aggregated.get(roundedPrice) || 0;
        aggregated.set(roundedPrice, existing + parseFloat(qty));
    });
    
    return Array.from(aggregated.entries())
        .map(([price, qty]) => ({ price, qty }))
        .sort((a, b) => b.price - a.price);
}

// ============================================================================
// UI Helpers
// ============================================================================
function showLoading(show) {
    const el = document.getElementById('loading');
    if (show) {
        el.classList.remove('hidden');
    } else {
        el.classList.add('hidden');
    }
}

function updateLoadingText(text) {
    const el = document.getElementById('loading-text');
    if (el) el.textContent = text;
}

// ============================================================================
// Event Handlers
// ============================================================================
function setupEventHandlers() {
    // Reload button
    document.getElementById('load-btn')?.addEventListener('click', loadData);
    
    // Go to date button
    document.getElementById('go-to-date')?.addEventListener('click', loadData);
    
    // Timeframe change
    document.getElementById('tf-select')?.addEventListener('change', loadData);
    
    // Exchange change
    document.getElementById('exchange-select')?.addEventListener('change', loadData);
    
    // Candle count change (with debounce)
    let candleTimeout;
    document.getElementById('candle-limit')?.addEventListener('change', () => {
        clearTimeout(candleTimeout);
        candleTimeout = setTimeout(loadData, 500);
    });
    
    // Toggle buttons
    document.getElementById('show-candles')?.addEventListener('click', (e) => {
        showCandles = !showCandles;
        e.target.classList.toggle('active', showCandles);
        candleSeries?.applyOptions({ visible: showCandles });
    });
    
    document.getElementById('show-footprint')?.addEventListener('click', (e) => {
        showFootprint = !showFootprint;
        e.target.classList.toggle('active', showFootprint);
        if (currentData) {
            drawFootprint(currentData.candles || []);
        }
    });
    
    document.getElementById('show-poc')?.addEventListener('click', (e) => {
        showPOC = !showPOC;
        e.target.classList.toggle('active', showPOC);
        if (currentData) {
            drawFootprint(currentData.candles || []);
        }
    });
    
    document.getElementById('show-va')?.addEventListener('click', (e) => {
        showVA = !showVA;
        e.target.classList.toggle('active', showVA);
        if (currentData) {
            drawFootprint(currentData.candles || []);
        }
    });
    
    document.getElementById('show-bubbles')?.addEventListener('click', (e) => {
        showBubbles = !showBubbles;
        e.target.classList.toggle('active', showBubbles);
        document.getElementById('bubble-slider-group')?.classList.toggle('visible', showBubbles);
    });
    
    document.getElementById('show-heatmap')?.addEventListener('click', (e) => {
        showHeatmap = !showHeatmap;
        e.target.classList.toggle('active', showHeatmap);
        document.getElementById('heatmap-controls')?.classList.toggle('visible', showHeatmap);
    });
    
    document.getElementById('show-orderflow')?.addEventListener('click', (e) => {
        showOrderFlow = !showOrderFlow;
        e.target.classList.toggle('active', showOrderFlow);
    });
    
    document.getElementById('autoscale-toggle')?.addEventListener('click', (e) => {
        autoScaleY = !autoScaleY;
        e.target.classList.toggle('active', autoScaleY);
        mainChart?.applyOptions({
            rightPriceScale: { autoScale: autoScaleY }
        });
    });
    
    document.getElementById('vol-unit-toggle')?.addEventListener('click', (e) => {
        volumeInUSD = !volumeInUSD;
        e.target.textContent = volumeInUSD ? 'USD' : 'BTC';
        if (currentData) {
            setCandleData(currentData.candles || []);
        }
    });
    
    // Indicator mode buttons
    document.querySelectorAll('.indicator-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.indicator-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            indicatorMode = e.target.dataset.mode;
            
            deltaSeries?.applyOptions({ visible: indicatorMode === 'delta' });
            cvdSeries?.applyOptions({ visible: indicatorMode === 'cvd' });
        });
    });
    
    // Record button - starts order book streaming
    document.getElementById('record-btn')?.addEventListener('click', async () => {
        isRecording = !isRecording;
        const btn = document.getElementById('record-btn');
        const status = document.getElementById('record-status');
        btn?.classList.toggle('recording', isRecording);
        
        if (isRecording) {
            if (status) {
                status.textContent = 'Starting...';
                status.classList.add('active');
            }
            await startOrderBookStreaming();
            if (status) status.textContent = 'Recording...';
        } else {
            disconnectOrderBookWebSocket();
            if (status) {
                status.textContent = 'Stopped';
                status.classList.remove('active');
            }
        }
    });
    
    // DOM aggregation change
    document.getElementById('dom-aggregation')?.addEventListener('change', () => {
        renderOrderBook();
    });
    
    // Heatmap opacity slider
    document.getElementById('heatmap-opacity')?.addEventListener('input', (e) => {
        const display = document.getElementById('heatmap-opacity-display');
        if (display) display.textContent = e.target.value + '%';
    });
    
    // Subscribe to chart visible range changes to redraw footprint
    mainChart?.timeScale().subscribeVisibleLogicalRangeChange(() => {
        if (currentData && showFootprint) {
            requestAnimationFrame(() => drawFootprint(currentData.candles || []));
        }
    });
    
    // Subscribe to crosshair move for footprint redraw on zoom/pan
    mainChart?.subscribeCrosshairMove(() => {
        // Throttled redraw will handle this
    });
}

// ============================================================================
// Initialization
// ============================================================================
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Total Core V2 initializing...');
    
    // Set default date to today
    const today = new Date().toISOString().split('T')[0];
    const dateInput = document.getElementById('start-date');
    if (dateInput) dateInput.value = today;
    
    // Initialize charts
    const success = await initCharts();
    if (!success) return;
    
    // Setup event handlers
    setupEventHandlers();
    
    // Load initial data
    await loadData();
    
    console.log('Total Core V2 ready');
});
