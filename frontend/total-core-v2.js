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
let logScale = false;
let volumeInUSD = true;

// Live streaming
let isRecording = false;
let orderbookWebSocket = null;
let currentOrderBook = { bids: [], asks: [] };

// Bubble data
let bubbleData = [];
let bubbleMinSize = 100000;  // $100K minimum
let bubbleMaxSize = 2000000; // $2M maximum

// Heatmap data (historical order book depth)
let heatmapData = [];
let heatmapOpacity = 0.6;

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
        url += `&start_ts=${startMs}`;
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
        
        // Load bubbles if enabled
        if (showBubbles) {
            loadBubbles();
        }
        
        // Load heatmap if enabled
        if (showHeatmap) {
            loadHeatmap();
        }
        
        // Load historical order book for Bybit
        if (exchange === 'bybit' && data.candles?.length > 0) {
            const lastCandle = data.candles[data.candles.length - 1];
            loadHistoricalOrderBook(lastCandle.timestamp);
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
    
    // Draw heatmap first (background layer)
    if (showHeatmap && heatmapData.length > 0) {
        drawHeatmap();
    }
    
    // Draw Order Flow OR Footprint (mutually exclusive)
    if (showOrderFlow && !showFootprint && candles.length > 0) {
        drawOrderFlow(candles);
    } else if (showFootprint && candles.length > 0) {
        drawFootprintCells(candles);
    }
    
    // Draw bubbles on top if enabled
    if (showBubbles && bubbleData.length > 0) {
        drawBubbles();
    }
}

// Draw footprint cells (extracted from main drawFootprint function)
function drawFootprintCells(candles) {
    const canvas = document.getElementById('footprint-canvas');
    if (!canvas || !mainChart || !candleSeries) return;
    
    const ctx = canvas.getContext('2d');
    const timeScale = mainChart.timeScale();
    
    const tickSize = currentData?.tick_size || 1;
    
    candles.forEach((candle, idx) => {
        // API returns 'profiles' not 'profile'
        let profiles = candle.profiles || candle.profile || [];
        if (!profiles.length) return;
        
        // Sort profiles by price for diagonal imbalance calculation
        profiles = [...profiles].sort((a, b) => a.price - b.price);
        
        const time = Math.floor(candle.timestamp / 1000);
        const x = timeScale.timeToCoordinate(time);
        if (x === null) return;
        
        // Get candle width (approximate)
        const nextTime = idx < candles.length - 1 
            ? Math.floor(candles[idx + 1].timestamp / 1000) 
            : time + 60;
        const nextX = timeScale.timeToCoordinate(nextTime);
        const candleWidth = nextX !== null ? Math.abs(nextX - x) * 0.85 : 20;
        const halfWidth = candleWidth / 2;
        
        // Find max volume for scaling
        const maxVol = Math.max(...profiles.map(p => p.total_volume || 0), 1);
        
        // Draw each price level as TWO-COLUMN (Bid | Ask) footprint
        profiles.forEach((level, levelIdx) => {
            const priceY = candleSeries.priceToCoordinate(level.price);
            if (priceY === null) return;
            
            const nextPriceY = candleSeries.priceToCoordinate(level.price + tickSize);
            const rowHeight = nextPriceY !== null ? Math.abs(nextPriceY - priceY) : 3;
            
            const bidVol = level.sell_volume || 0;  // Sellers hit bid
            const askVol = level.buy_volume || 0;   // Buyers lift ask
            const totalVol = bidVol + askVol;
            const horizontalDelta = askVol - bidVol;
            const isPOC = candle.poc && Math.abs(level.price - candle.poc) < tickSize / 2;
            
            // === BACKGROUND COLOR (horizontal delta) ===
            // Green = more buying, Purple = more selling
            let cellBg;
            if (totalVol === 0) {
                cellBg = 'rgba(100, 100, 110, 0.3)';
            } else {
                const imbalanceRatio = Math.abs(horizontalDelta) / totalVol;
                if (imbalanceRatio < 0.15) {
                    cellBg = 'rgba(110, 110, 120, 0.5)';  // Balanced
                } else if (horizontalDelta > 0) {
                    // More ask (buying) - GREEN pastel
                    const intensity = Math.min(imbalanceRatio * 1.5, 1);
                    cellBg = `rgba(80, ${180 + intensity * 60}, 120, ${0.4 + intensity * 0.3})`;
                } else {
                    // More bid (selling) - PURPLE/PINK pastel
                    const intensity = Math.min(imbalanceRatio * 1.5, 1);
                    cellBg = `rgba(${180 + intensity * 50}, 80, ${160 + intensity * 60}, ${0.4 + intensity * 0.3})`;
                }
            }
            
            // Draw cell background
            ctx.fillStyle = cellBg;
            ctx.fillRect(x - halfWidth, priceY - rowHeight / 2, candleWidth, Math.max(rowHeight - 1, 2));
            
            // POC yellow border
            if (isPOC && showPOC) {
                ctx.strokeStyle = COLORS.poc;
                ctx.lineWidth = 2;
                ctx.strokeRect(x - halfWidth, priceY - rowHeight / 2, candleWidth, Math.max(rowHeight - 1, 2));
            }
            
            // === TEXT COLORS (diagonal imbalance - 200% threshold) ===
            let bidTextColor = '#cccccc';
            let askTextColor = '#cccccc';
            
            // Check bid imbalance: bid[i] vs ask[i-1]
            if (levelIdx > 0 && bidVol > 0) {
                const askBelow = profiles[levelIdx - 1].buy_volume || 0;
                if (askBelow > 0 && bidVol >= askBelow * 2) {
                    bidTextColor = '#ff66ff';  // Magenta - sell imbalance
                }
            }
            
            // Check ask imbalance: ask[i] vs bid[i+1]
            if (levelIdx < profiles.length - 1 && askVol > 0) {
                const bidAbove = profiles[levelIdx + 1].sell_volume || 0;
                if (bidAbove > 0 && askVol >= bidAbove * 2) {
                    askTextColor = '#00ccff';  // Cyan - buy imbalance
                }
            }
            
            // Draw volume text if space allows
            if (rowHeight > 8 && candleWidth > 30) {
                ctx.font = `${Math.min(rowHeight - 2, 10)}px monospace`;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                
                // Bid volume (left column)
                if (bidVol > 0) {
                    ctx.fillStyle = bidTextColor;
                    ctx.fillText(bidVol >= 1 ? Math.round(bidVol).toString() : bidVol.toFixed(2), x - halfWidth / 2, priceY);
                }
                
                // Ask volume (right column)
                if (askVol > 0) {
                    ctx.fillStyle = askTextColor;
                    ctx.fillText(askVol >= 1 ? Math.round(askVol).toString() : askVol.toFixed(2), x + halfWidth / 2, priceY);
                }
            }
        });
        
        // Draw VA lines if enabled
        if (showVA && candle.vah && candle.val) {
            ctx.strokeStyle = COLORS.vah;
            ctx.lineWidth = 1.5;
            const vahY = candleSeries.priceToCoordinate(candle.vah);
            if (vahY !== null) {
                ctx.beginPath();
                ctx.moveTo(x - halfWidth, vahY);
                ctx.lineTo(x + halfWidth, vahY);
                ctx.stroke();
            }
            
            ctx.strokeStyle = COLORS.val;
            const valY = candleSeries.priceToCoordinate(candle.val);
            if (valY !== null) {
                ctx.beginPath();
                ctx.moveTo(x - halfWidth, valY);
                ctx.lineTo(x + halfWidth, valY);
                ctx.stroke();
            }
        }
    });
}

// ============================================================================
// Order Flow Visualization
// ============================================================================
function drawOrderFlow(candles) {
    const canvas = document.getElementById('footprint-canvas');
    if (!canvas || !mainChart || !candleSeries) return;
    
    const ctx = canvas.getContext('2d');
    const timeScale = mainChart.timeScale();
    const tickSize = currentData?.tick_size || 1;
    
    candles.forEach((candle, idx) => {
        let profiles = candle.profiles || candle.profile || [];
        if (!profiles.length) return;
        
        profiles = [...profiles].sort((a, b) => a.price - b.price);
        
        const time = Math.floor(candle.timestamp / 1000);
        const x = timeScale.timeToCoordinate(time);
        if (x === null) return;
        
        // Get candle width
        const nextTime = idx < candles.length - 1 
            ? Math.floor(candles[idx + 1].timestamp / 1000) 
            : time + 60;
        const nextX = timeScale.timeToCoordinate(nextTime);
        const candleWidth = nextX !== null ? Math.abs(nextX - x) * 0.85 : 20;
        
        // Find max volume for scaling
        const maxVol = Math.max(...profiles.map(p => p.total_volume || 0));
        if (maxVol === 0) return;
        
        // Find price range
        const minPrice = Math.min(...profiles.map(p => p.price));
        const maxPrice = Math.max(...profiles.map(p => p.price));
        
        // Draw vertical center line
        const minY = candleSeries.priceToCoordinate(maxPrice + tickSize);
        const maxY = candleSeries.priceToCoordinate(minPrice);
        if (minY !== null && maxY !== null) {
            ctx.beginPath();
            ctx.moveTo(x, minY);
            ctx.lineTo(x, maxY);
            ctx.strokeStyle = '#8888ff';
            ctx.lineWidth = 2;
            ctx.stroke();
        }
        
        // Max bar width = 45% of candle width
        const maxBarWidth = candleWidth * 0.45;
        
        profiles.forEach(profile => {
            const priceY = candleSeries.priceToCoordinate(profile.price);
            const priceY2 = candleSeries.priceToCoordinate(profile.price + tickSize);
            if (priceY === null || priceY2 === null) return;
            
            const bidVol = profile.sell_volume || 0;
            const askVol = profile.buy_volume || 0;
            const totalVol = bidVol + askVol;
            if (totalVol === 0) return;
            
            const isPOC = candle.poc && Math.abs(profile.price - candle.poc) < tickSize / 2;
            
            // Bar width proportional to volume
            const barWidth = (totalVol / maxVol) * maxBarWidth;
            
            // Color based on delta
            const delta = askVol - bidVol;
            let barColor;
            if (delta > 0) {
                const intensity = Math.min(Math.abs(delta) / totalVol, 1);
                barColor = `rgba(38, 166, 154, ${0.6 + intensity * 0.35})`;  // Teal
            } else if (delta < 0) {
                const intensity = Math.min(Math.abs(delta) / totalVol, 1);
                barColor = `rgba(186, 104, 200, ${0.6 + intensity * 0.35})`;  // Purple
            } else {
                barColor = 'rgba(150, 150, 150, 0.6)';
            }
            
            // Draw bar extending right from center
            const barHeight = Math.abs(priceY2 - priceY);
            ctx.fillStyle = barColor;
            ctx.fillRect(x, Math.min(priceY, priceY2), barWidth, barHeight);
            
            // Border
            ctx.strokeStyle = isPOC ? '#ffff00' : '#555555';
            ctx.lineWidth = isPOC ? 2 : 1;
            ctx.strokeRect(x, Math.min(priceY, priceY2), barWidth, barHeight);
            
            // Volume text if bar is wide enough and row is tall enough
            if (barWidth > 20 && barHeight > 10) {
                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 9px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                // Format as USD value (volume * price)
                const usdValue = totalVol * profile.price;
                let text;
                if (usdValue >= 1000000) {
                    text = (usdValue / 1000000).toFixed(1) + 'M';
                } else if (usdValue >= 1000) {
                    text = Math.round(usdValue / 1000) + 'K';
                } else {
                    text = Math.round(usdValue).toString();
                }
                ctx.fillText(text, x + barWidth / 2, (priceY + priceY2) / 2);
            }
        });
    });
}

// ============================================================================
// Bubble Visualization
// ============================================================================
async function loadBubbles() {
    if (!currentData?.candles?.length || !mainChart) return;
    
    const symbol = document.getElementById('symbol-select')?.value || 'BTCUSDT';
    const exchange = document.getElementById('exchange-select')?.value || 'binance';
    
    // Use candle time range (bubbles can only be drawn where we have candles)
    const candles = currentData.candles;
    const startTs = candles[0]?.timestamp;
    const endTs = candles[candles.length - 1]?.timestamp;
    
    if (!startTs || !endTs) return;
    
    try {
        const url = `/api/heatmap/bubbles?symbol=${symbol}&exchange=${exchange}&start_ts=${startTs}&end_ts=${endTs}&min_size_usd=${bubbleMinSize}&max_size_usd=${bubbleMaxSize}&limit=500`;
        const response = await fetch(url);
        if (!response.ok) return;
        
        const data = await response.json();
        bubbleData = data.bubbles || [];
        console.log(`Loaded ${bubbleData.length} bubbles`);
        
        drawBubbles();
    } catch (e) {
        console.error('Failed to load bubbles:', e);
    }
}

function updateBubbleRange() {
    const minSlider = document.getElementById('bubble-min-slider');
    const maxSlider = document.getElementById('bubble-max-slider');
    const display = document.getElementById('bubble-value-display');
    
    if (!minSlider || !maxSlider) return;
    
    let minVal = parseInt(minSlider.value);
    let maxVal = parseInt(maxSlider.value);
    
    // Ensure min <= max
    if (minVal > maxVal) {
        [minVal, maxVal] = [maxVal, minVal];
    }
    
    bubbleMinSize = minVal * 1000;  // Convert K to actual
    bubbleMaxSize = maxVal * 1000;
    
    if (display) {
        display.textContent = `${minVal}K - ${maxVal >= 1000 ? (maxVal/1000).toFixed(0) + 'M' : maxVal + 'K'}`;
    }
    
    // Reload bubbles with new range
    if (showBubbles && currentData) {
        loadBubbles();
    }
}

function drawBubbles() {
    const canvas = document.getElementById('footprint-canvas');
    if (!canvas || !mainChart || !candleSeries || !showBubbles) return;
    
    const ctx = canvas.getContext('2d');
    const timeScale = mainChart.timeScale();
    
    // Find size range for normalization (API returns quote_qty as USD value)
    const sizes = bubbleData.map(b => b.quote_qty);
    if (sizes.length === 0) return;
    const minSize = Math.min(...sizes);
    const maxSize = Math.max(...sizes);
    
    // Count how many bubbles are actually drawn
    let drawnCount = 0;
    
    // Build a map of candle times for quick lookup
    const candleTimes = currentData?.candles?.map(c => Math.floor(c.timestamp / 1000)) || [];
    
    bubbleData.forEach(bubble => {
        const bubbleTime = Math.floor(bubble.timestamp_ms / 1000);
        
        // Find the closest candle time for this bubble
        let closestCandleTime = candleTimes[0];
        for (const ct of candleTimes) {
            if (ct <= bubbleTime) closestCandleTime = ct;
            else break;
        }
        
        const x = timeScale.timeToCoordinate(closestCandleTime);
        const y = candleSeries.priceToCoordinate(bubble.price);
        
        if (x === null || y === null) return;
        
        // Calculate bubble radius based on size (8-35px)
        const sizeRatio = (bubble.quote_qty - minSize) / (maxSize - minSize + 1);
        const radius = 8 + sizeRatio * 27;
        
        // Color based on buy/sell
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fillStyle = bubble.is_buy 
            ? 'rgba(38, 166, 154, 0.6)' 
            : 'rgba(239, 83, 80, 0.6)';
        ctx.fill();
        
        // Add border
        ctx.strokeStyle = bubble.is_buy ? '#26a69a' : '#ef5350';
        ctx.lineWidth = 1;
        ctx.stroke();
        drawnCount++;
    });
    
}

// ============================================================================
// Heatmap Visualization (Historical Order Book Depth)
// ============================================================================
async function loadHeatmap() {
    if (!currentData?.candles?.length) return;
    
    const exchange = document.getElementById('exchange-select')?.value || 'binance';
    if (exchange !== 'bybit') {
        console.log("Heatmap only available for Bybit (has historical order book data)");
        return;
    }
    
    const candles = currentData.candles;
    const startTs = candles[0]?.timestamp;
    const endTs = candles[candles.length - 1]?.timestamp;
    
    if (!startTs || !endTs) return;
    
    try {
        // Get aggregated depth data for the time range
        const url = `/api/heatmap/bybit/depth?start_ts=${startTs}&end_ts=${endTs}&price_bucket=10&time_bucket_ms=60000&max_snapshots=500`;
        const response = await fetch(url);
        if (!response.ok) {
            console.log("No heatmap data available for this time range");
            return;
        }
        
        const data = await response.json();
        // API returns flat list: [{timestamp, side, price, size, mid}, ...]
        // Group by timestamp into buckets with bids/asks arrays
        const rawData = data.data || [];
        const bucketMap = new Map();
        
        rawData.forEach(entry => {
            const ts = entry.timestamp;
            if (!bucketMap.has(ts)) {
                bucketMap.set(ts, { timestamp: ts, bids: [], asks: [] });
            }
            const bucket = bucketMap.get(ts);
            if (entry.side === 'bid') {
                bucket.bids.push([entry.price, entry.size]);
            } else {
                bucket.asks.push([entry.price, entry.size]);
            }
        });
        
        heatmapData = Array.from(bucketMap.values()).sort((a, b) => a.timestamp - b.timestamp);
        console.log(`Loaded heatmap: ${heatmapData.length} time buckets from ${rawData.length} data points`);
        
        drawFootprint(currentData.candles || []);
    } catch (e) {
        console.error('Failed to load heatmap:', e);
    }
}

function drawHeatmap() {
    const canvas = document.getElementById('footprint-canvas');
    if (!canvas || !mainChart || !candleSeries || !showHeatmap || !heatmapData.length) return;
    
    const ctx = canvas.getContext('2d');
    const timeScale = mainChart.timeScale();
    
    // Get opacity from slider
    const opacitySlider = document.getElementById('heatmap-opacity');
    const opacity = opacitySlider ? parseInt(opacitySlider.value) / 100 : 0.6;
    
    // Find max quantity for color scaling (use 90th percentile for better contrast)
    const allQtys = [];
    heatmapData.forEach(bucket => {
        if (bucket.bids) bucket.bids.forEach(([price, qty]) => allQtys.push(qty));
        if (bucket.asks) bucket.asks.forEach(([price, qty]) => allQtys.push(qty));
    });
    allQtys.sort((a, b) => a - b);
    const maxQty = allQtys[Math.floor(allQtys.length * 0.9)] || allQtys[allQtys.length - 1] || 1;
    
    if (maxQty === 0) return;
    
    // Build candle time array for mapping
    const candleTimes = currentData?.candles?.map(c => Math.floor(c.timestamp / 1000)) || [];
    if (candleTimes.length === 0) return;
    
    // Get tick size for proper row height
    const tickSize = currentData?.tick_size || 10;
    
    heatmapData.forEach((bucket, idx) => {
        const bucketTime = Math.floor(bucket.timestamp / 1000);
        
        // Find closest candle time
        let closestCandleTime = candleTimes[0];
        for (const ct of candleTimes) {
            if (ct <= bucketTime) closestCandleTime = ct;
            else break;
        }
        
        const x = timeScale.timeToCoordinate(closestCandleTime);
        if (x === null) return;
        
        // Get candle width for bar width
        const candleIdx = candleTimes.indexOf(closestCandleTime);
        const nextCandleTime = candleIdx < candleTimes.length - 1 
            ? candleTimes[candleIdx + 1]
            : closestCandleTime + 60;
        const nextX = timeScale.timeToCoordinate(nextCandleTime);
        const barWidth = nextX !== null ? Math.abs(nextX - x) : 10;
        
        // Draw bid depth (green-cyan gradient based on intensity)
        if (bucket.bids) {
            bucket.bids.forEach(([price, qty]) => {
                const y = candleSeries.priceToCoordinate(price);
                const y2 = candleSeries.priceToCoordinate(price - tickSize);
                if (y === null || y2 === null) return;
                
                const rowHeight = Math.abs(y2 - y);
                const intensity = Math.min(qty / maxQty, 1);
                
                // Color gradient: dark green -> bright cyan for higher values
                const r = Math.floor(20 + intensity * 20);
                const g = Math.floor(80 + intensity * 120);
                const b = Math.floor(80 + intensity * 100);
                const alpha = 0.15 + intensity * opacity * 0.7;
                
                ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${alpha})`;
                ctx.fillRect(x - barWidth/2, Math.min(y, y2), barWidth, Math.max(rowHeight, 3));
            });
        }
        
        // Draw ask depth (red-orange gradient based on intensity)
        if (bucket.asks) {
            bucket.asks.forEach(([price, qty]) => {
                const y = candleSeries.priceToCoordinate(price);
                const y2 = candleSeries.priceToCoordinate(price + tickSize);
                if (y === null || y2 === null) return;
                
                const rowHeight = Math.abs(y2 - y);
                const intensity = Math.min(qty / maxQty, 1);
                
                // Color gradient: dark red -> bright orange for higher values
                const r = Math.floor(150 + intensity * 100);
                const g = Math.floor(40 + intensity * 80);
                const b = Math.floor(40 + intensity * 20);
                const alpha = 0.15 + intensity * opacity * 0.7;
                
                ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${alpha})`;
                ctx.fillRect(x - barWidth/2, Math.min(y, y2), barWidth, Math.max(rowHeight, 3));
            });
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

// Load historical order book for Bybit (since WebSocket only works for live data)
async function loadHistoricalOrderBook(timestamp) {
    const exchange = document.getElementById('exchange-select')?.value || 'binance';
    
    // Only Bybit has historical order book data
    if (exchange !== 'bybit') {
        console.log("Historical order book only available for Bybit");
        return null;
    }
    
    try {
        const url = `/api/heatmap/bybit/orderbook/snapshot?timestamp=${timestamp}&limit=100`;
        console.log(`Loading historical order book: ${url}`);
        const resp = await fetch(url);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        
        const data = await resp.json();
        if (data.error) {
            console.warn("No historical order book:", data.error);
            return null;
        }
        
        // Update currentOrderBook and render
        currentOrderBook = {
            bids: data.bids || [],
            asks: data.asks || []
        };
        renderOrderBook();
        console.log(`Loaded historical order book: ${data.bids?.length} bids, ${data.asks?.length} asks`);
        return data;
    } catch (err) {
        console.error("Failed to load historical order book:", err);
        return null;
    }
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
        // Footprint and Order Flow are mutually exclusive
        if (showFootprint && showOrderFlow) {
            showOrderFlow = false;
            document.getElementById('show-orderflow')?.classList.remove('active');
        }
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
        if (showBubbles && currentData) {
            loadBubbles();
        } else {
            // Redraw footprint without bubbles
            if (currentData) drawFootprint(currentData.candles || []);
        }
    });
    
    // Bubble size sliders
    document.getElementById('bubble-min-slider')?.addEventListener('input', updateBubbleRange);
    document.getElementById('bubble-max-slider')?.addEventListener('input', updateBubbleRange);
    
    document.getElementById('show-heatmap')?.addEventListener('click', (e) => {
        showHeatmap = !showHeatmap;
        e.target.classList.toggle('active', showHeatmap);
        document.getElementById('heatmap-controls')?.classList.toggle('visible', showHeatmap);
        if (showHeatmap && currentData) {
            loadHeatmap();
        } else {
            // Redraw without heatmap
            if (currentData) drawFootprint(currentData.candles || []);
        }
    });
    
    // Heatmap opacity slider
    document.getElementById('heatmap-opacity')?.addEventListener('input', (e) => {
        const display = document.getElementById('heatmap-opacity-display');
        if (display) display.textContent = e.target.value + '%';
        if (showHeatmap && currentData) {
            drawFootprint(currentData.candles || []);
        }
    });
    
    document.getElementById('show-orderflow')?.addEventListener('click', (e) => {
        showOrderFlow = !showOrderFlow;
        e.target.classList.toggle('active', showOrderFlow);
        // Order Flow and Footprint are mutually exclusive
        if (showOrderFlow && showFootprint) {
            showFootprint = false;
            document.getElementById('show-footprint')?.classList.remove('active');
        }
        if (currentData) {
            drawFootprint(currentData.candles || []);
        }
    });
    
    document.getElementById('autoscale-toggle')?.addEventListener('click', (e) => {
        autoScaleY = !autoScaleY;
        e.target.classList.toggle('active', autoScaleY);
        mainChart?.applyOptions({
            rightPriceScale: { autoScale: autoScaleY }
        });
    });
    
    // Log scale toggle (PriceScaleMode: 0=Normal, 1=Logarithmic)
    document.getElementById('log-toggle')?.addEventListener('click', (e) => {
        logScale = !logScale;
        e.target.classList.toggle('active', logScale);
        mainChart?.applyOptions({
            rightPriceScale: { mode: logScale ? 1 : 0 }
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
    
    // Subscribe to chart visible range changes to redraw canvas overlays
    mainChart?.timeScale().subscribeVisibleLogicalRangeChange(() => {
        if (currentData && (showFootprint || showOrderFlow || showHeatmap || showBubbles)) {
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
