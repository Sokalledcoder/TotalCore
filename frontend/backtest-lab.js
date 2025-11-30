const strategySelect = document.getElementById("strategy");
const engineSelect = document.getElementById("engine");
const paramFields = document.getElementById("paramFields");
const runsTableBody = document.querySelector("#runsTable tbody");
const runStatus = document.getElementById("runStatus");
const resultPanel = document.getElementById("resultPanel");
const metricsList = document.getElementById("metricsList");
const artifactLinks = document.getElementById("artifactLinks");

let strategySpecs = [];
let tfMinutes = 15;
let barLimit = 12000;
let lastJobId = null;

async function fetchJSON(url, options = {}) {
  const res = await fetch(url, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.json();
}

function renderParamFields(spec) {
  paramFields.innerHTML = "";
  if (!spec) return;
  spec.params.forEach((p) => {
    const wrapper = document.createElement("div");
    wrapper.className = "field";
    const label = document.createElement("label");
    label.textContent = `${p.name} (${p.type})`;
    label.setAttribute("for", `param-${p.name}`);
    const input = document.createElement("input");
    input.id = `param-${p.name}`;
    input.name = p.name;
    input.type = p.type === "float" ? "number" : p.type;
    input.step = p.step || "any";
    if (p.min !== null && p.min !== undefined) input.min = p.min;
    if (p.max !== null && p.max !== undefined) input.max = p.max;
    input.value = p.default;
    const hint = document.createElement("p");
    hint.className = "hint";
    hint.textContent = p.description;

    wrapper.appendChild(label);
    wrapper.appendChild(input);
    wrapper.appendChild(hint);
    paramFields.appendChild(wrapper);
  });
}

function syncEngineOptions(spec) {
  const supported = new Set(spec.engines);
  Array.from(engineSelect.options).forEach((opt) => {
    opt.disabled = !supported.has(opt.value);
  });
  if (engineSelect.options[engineSelect.selectedIndex]?.disabled) {
    const first = Array.from(engineSelect.options).find((o) => !o.disabled);
    if (first) engineSelect.value = first.value;
  }
}

async function loadStrategies() {
  strategySpecs = await fetchJSON("/api/backtests/strategies");
  strategySelect.innerHTML = "";
  strategySpecs.forEach((spec) => {
    const opt = document.createElement("option");
    opt.value = spec.id;
    opt.textContent = spec.label;
    strategySelect.appendChild(opt);
  });
  if (strategySpecs.length) {
    renderParamFields(strategySpecs[0]);
    syncEngineOptions(strategySpecs[0]);
  }
}

function getSelectedSpec() {
  return strategySpecs.find((s) => s.id === strategySelect.value);
}

function gatherParams(spec) {
  const params = {};
  spec.params.forEach((p) => {
    const el = document.getElementById(`param-${p.name}`);
    if (!el) return;
    const val = el.value;
    if (p.type === "int") params[p.name] = parseInt(val, 10);
    else if (p.type === "float") params[p.name] = parseFloat(val);
    else params[p.name] = val;
  });
  return params;
}

function isoOrNull(input) {
  const v = input.value;
  return v ? new Date(v).toISOString() : null;
}

async function submitBacktest(event) {
  event.preventDefault();
  const spec = getSelectedSpec();
  if (!spec) return;

  const payload = {
    strategy_id: spec.id,
    engine: engineSelect.value,
    params: gatherParams(spec),
    data: {
      exchange: document.getElementById("exchange").value,
      symbols: document
        .getElementById("symbols")
        .value.split(",")
        .map((s) => s.trim())
        .filter(Boolean),
      timeframe: document.getElementById("timeframe").value,
      start: isoOrNull(document.getElementById("start")),
      end: isoOrNull(document.getElementById("end")),
      limit: document.getElementById("limit").value
        ? Number(document.getElementById("limit").value)
        : null,
    },
    cv_config: {
      cash: Number(document.getElementById("cash").value) || 10000,
    },
    optimizer: {},
  };

  runStatus.textContent = "Submitting…";
  try {
    const job = await fetchJSON("/api/backtests/jobs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    runStatus.textContent = `Job ${job.id} queued`;
    pollJob(job.id);
    refreshRuns();
  } catch (err) {
    runStatus.textContent = `Error: ${err.message}`;
  }
}

async function pollJob(jobId) {
  let attempts = 0;
  const maxAttempts = 120; // ~2 min at 1s cadence
  const interval = setInterval(async () => {
    attempts += 1;
    try {
      const job = await fetchJSON(`/api/backtests/jobs/${jobId}`);
      renderJobResult(job);
      if (["completed", "failed"].includes(job.status) || attempts >= maxAttempts) {
        clearInterval(interval);
        refreshRuns();
        if (job.status === "completed") {
          runStatus.textContent = `Job ${job.id} done`;
        } else {
          runStatus.textContent = `Job ${job.id} failed: ${job.error || "Unknown error"}`;
        }
      } else {
        runStatus.textContent = `Job ${job.id} ${job.status} (${Math.round(job.progress * 100)}%)`;
      }
    } catch (err) {
      clearInterval(interval);
      runStatus.textContent = `Error polling: ${err.message}`;
    }
  }, 1000);
}

function renderJobResult(job) {
  if (!job || job.status !== "completed") return;
  lastJobId = job.id;
  resultPanel.style.display = "block";
  document.getElementById("chartPanel").style.display = "block";
  metricsList.innerHTML = "";
  const metrics = job.metrics || {};
  const priority = [
    "Return [%]",
    "CAGR [%]",
    "Sharpe Ratio",
    "Max. Drawdown [%]",
    "Exposure Time [%]",
    "Win Rate [%]",
    "Profit Factor",
    "# Trades",
  ];
  const orderedKeys = [
    ...priority.filter((k) => k in metrics),
    ...Object.keys(metrics).filter((k) => !priority.includes(k)),
  ];
  const mid = Math.ceil(orderedKeys.length / 2);
  const columns = [orderedKeys.slice(0, mid), orderedKeys.slice(mid)];
  const grid = document.createElement("div");
  grid.className = "metrics-grid";
  columns.forEach((keys) => {
    const table = document.createElement("table");
    table.className = "compact";
    const tbody = document.createElement("tbody");
    keys.forEach((k) => {
      const tr = document.createElement("tr");
      const key = document.createElement("td");
      key.textContent = k;
      const val = document.createElement("td");
      const v = metrics[k];
      val.textContent =
        typeof v === "number" && isFinite(v) ? (Math.abs(v) >= 10 ? v.toFixed(2) : v.toFixed(4)) : String(v);
      tr.appendChild(key);
      tr.appendChild(val);
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    grid.appendChild(table);
  });
  metricsList.appendChild(grid);

  artifactLinks.innerHTML = "";
const artifacts = job.artifacts || {};
  Object.entries(artifacts).forEach(([k, path]) => {
    const a = document.createElement("a");
    a.href = `/api/backtests/jobs/${job.id}/artifacts/${k}`;
    a.textContent = k;
    a.target = "_blank";
    artifactLinks.appendChild(a);
  });

  if (artifacts.chart_preview) {
    renderChart(job.id);
  }
}

async function renderChart(jobId) {
  const container = document.getElementById("chartContainer");
  container.innerHTML = "";
  const res = await fetch(`/api/backtests/jobs/${jobId}/artifacts/chart_preview`);
  if (!res.ok) {
    container.textContent = "Chart preview unavailable";
    return;
  }
  const data = await res.json();
  let { price = [], indicators = {}, trades = [] } = data;
  if (!price.length) {
    container.textContent = "No price data to render.";
    return;
  }
  // Aggregate candles to selected timeframe (minutes)
  const bucketSec = Math.max(1, tfMinutes) * 60;
  const buckets = new Map();
  for (const p of price) {
    const t = Number(p.t);
    const bucket = Math.floor(t / bucketSec) * bucketSec;
    const existing = buckets.get(bucket);
    if (!existing) {
      buckets.set(bucket, { t: bucket, o: p.o, h: p.h, l: p.l, c: p.c });
    } else {
      existing.h = Math.max(existing.h, p.h);
      existing.l = Math.min(existing.l, p.l);
      existing.c = p.c;
    }
  }
  price = Array.from(buckets.values()).sort((a, b) => a.t - b.t);
  // Optional bar limit
  if (barLimit > 0 && price.length > barLimit) {
    price = price.slice(-barLimit);
    Object.keys(indicators).forEach((k) => {
      indicators[k] = indicators[k]?.slice?.(-barLimit) || indicators[k];
    });
    if (trades?.length) {
      const cutoff = price[0].t;
      trades = trades.filter((t) => Number(t.entry_t) >= cutoff || Number(t.exit_t) >= cutoff);
    }
  }
  const chart = echarts.init(container, null, { renderer: "canvas" });
  const ohlc = price.map(p => [Number(p.t) * 1000, Number(p.o), Number(p.c), Number(p.l), Number(p.h)]);
  const series = [
    {
      type: 'candlestick',
      name: 'Price',
      data: ohlc,
      itemStyle: {
        color: '#16a34a',
        color0: '#ef4444',
        borderColor: '#16a34a',
        borderColor0: '#ef4444',
      },
    },
  ];

  if (indicators.ma_fast) {
    series.push({
      type: 'line',
      name: 'MA Fast',
      data: indicators.ma_fast.filter(p => p.v !== null).map(p => [Number(p.t) * 1000, p.v]),
      showSymbol: false,
      lineStyle: { width: 2, color: '#4ade80' },
    });
  }
  if (indicators.ma_slow) {
    series.push({
      type: 'line',
      name: 'MA Slow',
      data: indicators.ma_slow.filter(p => p.v !== null).map(p => [Number(p.t) * 1000, p.v]),
      showSymbol: false,
      lineStyle: { width: 2, color: '#60a5fa' },
    });
  }

  const markPoints = [];
  trades.forEach(tr => {
    const side = String(tr.side || '').toLowerCase();
    const entryT = Number(tr.entry_t);
    const exitT = Number(tr.exit_t);
    const entryP = Number(tr.entry_price || tr.EntryPrice || tr.entry || price[0]?.o);
    const exitP = Number(tr.exit_price || tr.ExitPrice || tr.exit || price[price.length-1]?.c);
    if (tr.entry_t && !Number.isNaN(entryT) && !Number.isNaN(entryP)) {
      markPoints.push({
        name: 'Entry',
        coord: [entryT * 1000, entryP],
        itemStyle: { color: side.includes('short') ? '#ef4444' : '#22c55e' },
      });
    }
    if (tr.exit_t && !Number.isNaN(exitT) && !Number.isNaN(exitP)) {
      markPoints.push({
        name: 'Exit',
        coord: [exitT * 1000, exitP],
        itemStyle: { color: side.includes('short') ? '#22c55e' : '#ef4444' },
      });
    }
  });
  if (markPoints.length) {
    series[0].markPoint = { data: markPoints, symbolSize: 28 };
  }

  chart.setOption({
    animation: false,
    backgroundColor: '#0f1115',
    tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
    legend: { textStyle: { color: '#dfe3eb' } },
    grid: { left: 60, right: 40, top: 40, bottom: 80 },
    xAxis: {
      type: 'time',
      axisLine: { lineStyle: { color: '#2a2f3a' } },
      axisLabel: { color: '#dfe3eb' },
      splitLine: { lineStyle: { color: '#1b1e24' } },
    },
    yAxis: {
      scale: true,
      axisLine: { lineStyle: { color: '#2a2f3a' } },
      axisLabel: { color: '#dfe3eb' },
      splitLine: { lineStyle: { color: '#1b1e24' } },
    },
    dataZoom: [
      { type: 'inside', xAxisIndex: 0 },
      { type: 'slider', xAxisIndex: 0, bottom: 20, height: 20 },
    ],
    series,
  });
}

function formatTimestamp(ts) {
  try {
    return new Date(ts).toLocaleString();
  } catch {
    return ts;
  }
}

function renderRuns(rows) {
  runsTableBody.innerHTML = "";
  rows.forEach((row) => {
    const tr = document.createElement("tr");
    tr.dataset.id = row.id;
    if (row.id === lastJobId) {
      tr.classList.add("selected");
    }
    tr.innerHTML = `
      <td>${row.id}</td>
      <td>${row.strategy_id}</td>
      <td>${row.engine}</td>
      <td class="${row.status}">${row.status}</td>
      <td>${formatTimestamp(row.updated_at)}</td>
      <td>${row.metrics && Object.keys(row.metrics).length ? Object.keys(row.metrics).slice(0,4).join(", ") : "-"}</td>
      <td><button class="ghost danger" data-id="${row.id}">Delete</button></td>
    `;
    tr.addEventListener("click", () => {
      runsTableBody.querySelectorAll("tr").forEach((r) => r.classList.remove("selected"));
      tr.classList.add("selected");
      renderJobResult(row);
    });
    runsTableBody.appendChild(tr);
  });
  runsTableBody.querySelectorAll("button[data-id]").forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.stopPropagation();
      const id = btn.dataset.id;
      if (!id) return;
      btn.disabled = true;
      try {
        await fetch(`/api/backtests/jobs/${id}`, { method: "DELETE" });
        refreshRuns();
      } catch (err) {
        console.error("Delete failed", err);
      } finally {
        btn.disabled = false;
      }
    });
  });
}

document.getElementById("tfSelect").addEventListener("change", (e) => {
  tfMinutes = Number(e.target.value) || 1;
  const selectedRow = runsTableBody.querySelector("tr.selected");
  const id = selectedRow?.dataset?.id || selectedRow?.firstChild?.textContent || lastJobId;
  if (id) renderChart(id.trim());
});

const barLimitSelect = document.getElementById("barLimit");
if (barLimitSelect) {
  barLimitSelect.addEventListener("change", (e) => {
  barLimit = Number(e.target.value) || 0;
  const selectedRow = runsTableBody.querySelector("tr.selected");
  const id = selectedRow?.dataset?.id || selectedRow?.firstChild?.textContent || lastJobId;
  if (id) renderChart(id.trim());
});

window.addEventListener("resize", () => {
  const container = document.getElementById("chartContainer");
  const chart = echarts.getInstanceByDom(container);
  if (chart) {
    chart.resize();
  }
});
}

async function refreshRuns() {
  try {
    const rows = await fetchJSON("/api/backtests/jobs?limit=50");
    if (!lastJobId && rows.length) {
      lastJobId = rows[0].id;
    }
    renderRuns(rows);
    if (lastJobId) {
      const selectedRow = runsTableBody.querySelector(`tr[data-id="${lastJobId}"]`);
      if (selectedRow) selectedRow.classList.add("selected");
    }
  } catch (err) {
    console.error("Failed to load runs", err);
  }
}

strategySelect.addEventListener("change", () => {
  const spec = getSelectedSpec();
  renderParamFields(spec);
  syncEngineOptions(spec);
});

document.getElementById("backtestForm").addEventListener("submit", submitBacktest);

loadStrategies().then(refreshRuns);
