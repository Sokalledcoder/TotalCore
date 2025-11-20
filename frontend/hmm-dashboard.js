const API_BASE = '/api/hmm';

const trainBtn = document.getElementById('trainBtn');
const refreshBtn = document.getElementById('refreshBtn');
const statsPanel = document.getElementById('statsPanel');
const startInput = document.getElementById('start_date');
const endInput = document.getElementById('end_date');
const tfRow = document.getElementById('tfRow');
const autoRefresh = document.getElementById('autoRefresh');
const lastPriceEl = document.getElementById('lastPrice');
const savedRuns = document.getElementById('savedRuns');
const loadRunBtn = document.getElementById('loadRun');
const deleteRunBtn = document.getElementById('deleteRun');
const candleLimitInput = document.getElementById('candleLimit');
const autoK = document.getElementById('autoK');
const kMinInput = document.getElementById('k_min');
const kMaxInput = document.getElementById('k_max');
const profileSel = document.getElementById('profile');

// Regime Colors
const REGIME_COLORS = {
    "Strong Bear": "#b30000",
    "Bear": "#e05555",
    "Chop": "#808080",
    "Chop 1": "#5c7a99",
    "Chop 2": "#556b2f",
    "Neutral": "#808080",
    "Bull": "#00cc66",
    "Strong Bull": "#00ff99"
};
const DEFAULT_COLOR = "#ffffff";

let priceTimer = null;
let dataTimer = null;

trainBtn.addEventListener('click', async () => {
    const exchange = document.getElementById('exchange').value;
    const symbol = document.getElementById('symbol').value;
    const timeframe = document.getElementById('timeframe').value;
    const n_states = parseInt(document.getElementById('n_states').value);
    const start_date = startInput.value || null;
    const end_date = endInput.value || null;
    let auto_k = autoK ? autoK.checked : false;
    let k_min = parseInt(kMinInput?.value || "2", 10);
    let k_max = parseInt(kMaxInput?.value || "4", 10);
    let strict_k = !auto_k; // if auto_k is off, enforce strict K
    let legacy = false;
    const profile = profileSel ? profileSel.value : 'legacy';

    // profile overrides
    if (profile === 'legacy') {
        auto_k = false;
        strict_k = true;
        legacy = true;
    } else if (profile === 'scaled') {
        auto_k = false;
        strict_k = true;
        legacy = false;
    } else if (profile === 'scaled_autok') {
        auto_k = true;
        strict_k = false;
        legacy = false;
    }

    trainBtn.disabled = true;
    trainBtn.textContent = "Training...";

    try {
        const res = await fetch(`${API_BASE}/train`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ exchange, symbol, timeframe, n_states, start_date, end_date, auto_k, k_min, k_max, strict_k, legacy, profile })
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail);
        }

        const data = await res.json();
        renderStats(data.stats, { timeframe, n_states: (data.diagnostics && data.diagnostics.k) || n_states, start_date, end_date, diagnostics: data.diagnostics, profile });
        alert("Training complete!");
        loadData(data.model_id); // Refresh charts with this model
    } catch (e) {
        alert(`Error: ${e.message}`);
    } finally {
        trainBtn.disabled = false;
        trainBtn.textContent = "Train Model";
    }
});

refreshBtn.addEventListener('click', () => loadData(getSelectedRunId()));
loadRunBtn.addEventListener('click', () => loadData(getSelectedRunId()));
deleteRunBtn.addEventListener('click', deleteSavedRun);
savedRuns?.addEventListener('change', loadSelectedRun);

populateRuns();

async function loadData(modelId = null) {
    const exchange = document.getElementById('exchange').value;
    const symbol = document.getElementById('symbol').value;
    const timeframe = document.getElementById('timeframe').value;
    const start_date = startInput.value || '';
    const end_date = endInput.value || '';
    const limit = parseInt(candleLimitInput?.value || '1000', 10);

    try {
        const query = new URLSearchParams({ exchange, symbol, timeframe, limit: limit, use_persisted: true });
        if (modelId) query.set('model_id', modelId);
        if (start_date) query.set('start_date', start_date);
        if (end_date) query.set('end_date', end_date);

        const res = await fetch(`${API_BASE}/regime?${query.toString()}`);
        if (!res.ok) throw new Error(`Failed to fetch regime data (${res.status})`);

        let payload = await res.json();
        let data = payload;
        if (payload && payload.data) {
            data = payload.data;
            if (payload.labels) {
                window.regimeLabels = payload.labels;
            }
        }

        renderCharts(data);
        renderProbStats(data);
    } catch (e) {
        console.error(e);
        alert(e.message);
    }
}

function getSelectedRunId() {
    const opt = savedRuns?.selectedOptions?.[0];
    return opt ? opt.value : null;
}

async function deleteSavedRun() {
    const id = getSelectedRunId();
    if (!id) return;
    if (!confirm(`Delete saved run ${id}?`)) return;
    await fetch(`${API_BASE}/models/${id}`, { method: 'DELETE' });
    await populateRuns();
}


function loadSelectedRun() {
    const opt = savedRuns?.selectedOptions?.[0];
    const modelId = opt ? opt.value : null;
    if (!modelId) return;
    // Align selectors to the saved run metadata
    if (opt.dataset.exchange) document.getElementById('exchange').value = opt.dataset.exchange;
    if (opt.dataset.symbol) document.getElementById('symbol').value = opt.dataset.symbol;
    if (opt.dataset.timeframe) document.getElementById('timeframe').value = opt.dataset.timeframe;
    setLoading(true);
    loadData(modelId).finally(() => setLoading(false));
}
function setLoading(isLoading) {
    if (isLoading) {
        loadRunBtn.textContent = 'Loading...';
        loadRunBtn.disabled = true;
        refreshBtn.disabled = true;
    } else {
        loadRunBtn.textContent = 'Load Run';
        loadRunBtn.disabled = false;
        refreshBtn.disabled = false;
    }
}

async function populateRuns() {
    try {
        const res = await fetch(`${API_BASE}/models`);
        if (!res.ok) return;
        const runs = await res.json();
        savedRuns.innerHTML = '';
        runs.forEach(r => {
            const opt = document.createElement('option');
            opt.value = r.id;
            opt.textContent = `${r.id} (${r.timeframe})`;
            opt.dataset.exchange = r.exchange;
            opt.dataset.symbol = r.symbol;
            opt.dataset.timeframe = r.timeframe;
            savedRuns.appendChild(opt);
        });
    } catch (e) {
        console.error(e);
    }
}

function renderStats(stats, meta = {}) {
    statsPanel.innerHTML = '';
    window.regimeLabels = {}; // Store for charts

    if (meta) {
        const info = document.createElement('div');
        info.className = 'stat-card';
        const windowText = meta.start_date || meta.end_date
            ? `${meta.start_date || '...'} → ${meta.end_date || 'now'}`
            : 'full history available';
        let diag = '';
        if (meta.diagnostics) {
            const d = meta.diagnostics;
            const stateCounts = d.state_counts ? d.state_counts.join(', ') : '';
            diag = `<br>K (used): ${d.k}<br>loglik train: ${d.loglik_train?.toFixed(2)}<br>loglik val: ${d.loglik_val?.toFixed(2)}<br>BIC: ${d.bic?.toFixed(2)}<br>state counts: ${stateCounts}`;
            if (d.mode) diag += `<br>mode: ${d.mode}`;
        }
        const profile = meta.profile ? `<br>profile: ${meta.profile}` : '';
        info.innerHTML = `<strong>Training Run</strong><br>
            Timeframe: ${meta.timeframe || 'N/A'}<br>
            States: ${meta.n_states || 'N/A'}<br>
            Window: ${windowText}${diag}${profile}`;
        statsPanel.appendChild(info);
    }

    for (const [state, metrics] of Object.entries(stats)) {
        const label = metrics.label || `Regime ${state}`;
        window.regimeLabels[state] = label;

        const color = getRegimeColor(label);

        const div = document.createElement('div');
        div.className = 'stat-card';
        div.style.borderLeft = `4px solid ${color}`;
        div.innerHTML = `
            <strong>${label}</strong><br>
            Avg Return: ${(metrics.avg_return * 100).toFixed(4)}%<br>
            Volatility: ${(metrics.volatility * 100).toFixed(4)}%<br>
            ADX: ${metrics.avg_adx.toFixed(2)}<br>
            RSI: ${metrics.avg_rsi.toFixed(2)}
        `;
        statsPanel.appendChild(div);
    }
}

function getRegimeColor(label) {
    for (const [key, color] of Object.entries(REGIME_COLORS)) {
        if (label.includes(key)) return color;
    }
    return DEFAULT_COLOR;
}

function renderCharts(data) {
    if (!data || !data.length) return;

    const times = data.map(d => d.timestamp);

    // 1. Candlestick Chart
    // To color candlesticks by regime, we need to create separate traces for each regime.
    // Or use a single trace and color array? Plotly candlestick colors are for up/down.
    // We can't easily color the whole candle by regime AND by up/down.
    // User asked: "color the candlesticks themselves".
    // Compromise: We can use the 'increasing' and 'decreasing' line colors, 
    // but that applies to the whole trace.
    // So we MUST split the data into multiple traces, one for each regime.

    const traces = [];
    const uniqueRegimes = [...new Set(data.map(d => d.regime))].sort();

    uniqueRegimes.forEach(r => {
        // Filter data for this regime
        // We need to be careful with gaps. Plotly handles gaps by connecting if we want, 
        // but for candlesticks, gaps are just missing candles.

        const regimeData = data.map((d, i) => d.regime === r ? d : null);

        // We need arrays for x, open, high, low, close
        const x = [], open = [], high = [], low = [], close = [];

        regimeData.forEach(d => {
            if (d) {
                x.push(d.timestamp);
                // We need OHLC. The API currently only returns 'price' (close).
                // I need to update the API to return OHLC for the dashboard.
                // Wait, the user said "I want to see the actual candlesticks".
                // My API /regime currently only returns 'price'.
                // I MUST UPDATE THE API TO RETURN OHLC.
                // For now, I will assume the API is updated.
                open.push(d.open);
                high.push(d.high);
                low.push(d.low);
                close.push(d.close);
            }
        });

        const label = window.regimeLabels ? window.regimeLabels[r] : `Regime ${r}`;
        const color = getRegimeColor(label);

        traces.push({
            x: x,
            open: open,
            high: high,
            low: low,
            close: close,
            type: 'candlestick',
            name: label,
            increasing: { line: { color: color } },
            decreasing: { line: { color: color } }
        });
    });

    const layoutPrice = {
        title: 'Price by Regime',
        paper_bgcolor: '#1e1e1e',
        plot_bgcolor: '#1e1e1e',
        font: { color: '#ddd' },
        xaxis: { gridcolor: '#333', rangeslider: { visible: false } },
        yaxis: { gridcolor: '#333' },
        showlegend: true
    };

    Plotly.newPlot('priceChart', traces, layoutPrice);

    // 2. Probability Chart
    const probTraces = [];
    const n_states = data[0].probs.length;

    for (let i = 0; i < n_states; i++) {
        const label = window.regimeLabels ? window.regimeLabels[i] : `Regime ${i}`;
        probTraces.push({
            x: times,
            y: data.map(d => d.probs[i]),
            stackgroup: 'one',
            name: label,
            line: { color: getRegimeColor(label) }
        });
    }

    const layoutProb = {
        title: 'Regime Probabilities',
        paper_bgcolor: '#1e1e1e',
        plot_bgcolor: '#1e1e1e',
        font: { color: '#ddd' },
        xaxis: { gridcolor: '#333' },
        yaxis: { range: [0, 1], gridcolor: '#333' }
    };

    Plotly.newPlot('probChart', probTraces, layoutProb);

    // Last price badge
    const last = data[data.length - 1];
    if (lastPriceEl) {
        const ts = new Date(last.timestamp).toLocaleString();
        lastPriceEl.textContent = `Last price: ${last.close.toFixed(2)} @ ${ts}`;
    }
}

// Quick timeframe buttons
tfRow?.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-tf]');
    if (!btn) return;
    const tf = btn.getAttribute('data-tf');
    document.getElementById('timeframe').value = tf;
    markActive(tfRow, tf, 'data-tf');
    loadData();
});

function markActive(container, value, attr) {
    container.querySelectorAll('[data-tf]').forEach(btn => btn.classList.remove('active'));
    const target = container.querySelector(`[${attr}="${value}"]`);
    if (target) target.classList.add('active');
}

// Auto-refresh toggle
autoRefresh?.addEventListener('change', () => {
    if (autoRefresh.checked) {
        if (priceTimer) clearInterval(priceTimer);
        priceTimer = setInterval(tickLivePrice, 10_000);
        tickLivePrice();
    } else {
        if (priceTimer) clearInterval(priceTimer);
        priceTimer = null;
    }
});

async function tickLivePrice() {
    const exchange = document.getElementById('exchange').value;
    const symbol = document.getElementById('symbol').value;
    const timeframe = document.getElementById('timeframe').value;
    try {
        const res = await fetch(`${API_BASE}/price/latest?exchange=${exchange}&symbol=${encodeURIComponent(symbol)}&timeframe=${timeframe}`);
        if (!res.ok) return;
        const p = await res.json();
        if (lastPriceEl) {
            const ts = new Date(p.timestamp).toLocaleString();
            lastPriceEl.textContent = `Live: ${p.close.toFixed(2)} @ ${ts}`;
        }
    } catch (e) {
        console.error(e);
    }
}


function renderProbStats(data) {
    const pane = document.getElementById('probStats');
    if (!pane) return;
    if (!data || !data.length) { pane.innerHTML = 'No data'; return; }
    const last = data[data.length - 1];
    const labels = window.regimeLabels || {};
    let rows = '';
    last.probs.forEach((p, idx) => {
        const label = labels[idx] || `Regime ${idx}`;
        rows += `<tr><td>${label}</td><td>${(p*100).toFixed(2)}%</td></tr>`;
    });
    pane.innerHTML = `
      <strong>Latest Probabilities</strong>
      <table style="width:100%; font-size:12px; margin-top:6px;">
        <tbody>${rows}</tbody>
      </table>
      <div style="margin-top:6px; font-size:12px;">Last bar: ${new Date(last.timestamp).toLocaleString()}</div>
    `;
}


async function fetchLatestProbs() {
    const opt = savedRuns?.selectedOptions?.[0];
    const modelId = opt ? opt.value : null;
    const exchange = document.getElementById('exchange').value;
    const symbol = document.getElementById('symbol').value;
    const timeframe = document.getElementById('timeframe').value;
    try {
        const url = modelId
            ? `${API_BASE}/latest?model_id=${modelId}`
            : `${API_BASE}/latest?exchange=${exchange}&symbol=${encodeURIComponent(symbol)}&timeframe=${timeframe}`;
        const res = await fetch(url);
        if (!res.ok) return;
        const payload = await res.json();
        // Update prob stats only
        const fakeData = [{
            timestamp: payload.timestamp,
            regime: payload.regime,
            probs: payload.probs,
            open: null, high: null, low: null, close: payload.price,
        }];
        window.regimeLabels = payload.labels || window.regimeLabels;
        renderProbStats(fakeData);
    } catch (e) {
        console.error(e);
    }
}
