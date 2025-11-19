const rewardCanvas = document.getElementById('rewardChart');
const throughputCanvas = document.getElementById('throughputChart');
const refreshBtn = document.getElementById('refreshInsights');
const runsTableBody = document.querySelector('#runsTable tbody');
const bestRewardEl = document.getElementById('bestReward');
const bestRewardTagEl = document.getElementById('bestRewardTag');
const selectedRewardEl = document.getElementById('selectedReward');
const selectedLabelEl = document.getElementById('selectedLabel');
const latestRunEl = document.getElementById('latestRun');
const latestRunTimeEl = document.getElementById('latestRunTime');
const avgStepsEl = document.getElementById('avgSteps');
const avgFpsEl = document.getElementById('avgFps');
const detailProfit = document.getElementById('detailProfit');
const detailReturn = document.getElementById('detailReturn');
const rewardMetricSelect = document.getElementById('rewardMetric');
const throughputMetricSelect = document.getElementById('throughputMetric');
const scatterCanvas = document.getElementById('scatterChart');
const detailPanel = document.getElementById('detailPanel');
const detailRunLabel = document.getElementById('detailRunLabel');
const detailTag = document.getElementById('detailTag');
const detailStatus = document.getElementById('detailStatus');
const detailDuration = document.getElementById('detailDuration');
const detailDurationExact = document.getElementById('detailDurationExact');
const detailSeed = document.getElementById('detailSeed');
const detailEpisodes = document.getElementById('detailEpisodes');
const detailEnv = document.getElementById('detailEnv');
const detailTrain = document.getElementById('detailTrain');
const detailRunDir = document.getElementById('detailRunDir');
const detailOverrides = document.getElementById('detailOverrides');
const detailFps = document.getElementById('detailFps');
const actionsPanel = document.getElementById('actionsPanel');
const actionMetricSelect = document.getElementById('actionMetric');
const actionEnvSelect = document.getElementById('actionEnv');
const actionPointsSelect = document.getElementById('actionPoints');
const actionChartCanvas = document.getElementById('actionChart');
const actionSummaryEl = document.getElementById('actionSummary');
const actionStatStart = document.getElementById('actionStatStart');
const actionStatEnd = document.getElementById('actionStatEnd');
const actionStatMinMax = document.getElementById('actionStatMinMax');
const actionStatMean = document.getElementById('actionStatMean');
const actionStatRows = document.getElementById('actionStatRows');
const actionLogPathEl = document.getElementById('actionLogPath');
const actionSampleBody = document.querySelector('#actionSample tbody');

const ACTION_METRICS = [
  'equity',
  'cash',
  'position',
  'drawdown',
  'episode_pnl_usd',
  'last_price',
  'decision_direction',
  'decision_size_fraction',
  'target_position',
];
const ACTION_METRIC_LABELS = {
  equity: 'Equity ($)',
  cash: 'Cash ($)',
  position: 'Position',
  drawdown: 'Drawdown %',
  episode_pnl_usd: 'Episode PnL ($)',
  last_price: 'Last Price',
  decision_direction: 'Decision Direction',
  decision_size_fraction: 'Size Fraction',
  target_position: 'Target Position',
};
const ACTION_SAMPLE_FIELDS = [
  'global_step',
  'env_index',
  'episode_step',
  'decision_direction',
  'decision_size_fraction',
  'target_position',
  'cash',
  'position',
  'equity',
  'drawdown',
  'episode_pnl_usd',
];
const currencyFormatter = new Intl.NumberFormat(undefined, {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 2,
});

let rewardChart;
let throughputChart;
let scatterChart;
let currentRuns = [];
let jobLookup = new Map();
let selectedRunId = null;
let actionChart;
const actionCache = new Map();
let currentActionData = null;
let currentActionMetric = 'equity';
let currentActionEnv = 'all';
let currentActionPoints = 1500;

refreshBtn?.addEventListener('click', () => loadInsights());
rewardMetricSelect?.addEventListener('change', () => renderCharts(currentRuns));
throughputMetricSelect?.addEventListener('change', () => renderCharts(currentRuns));
actionMetricSelect?.addEventListener('change', () => {
  currentActionMetric = actionMetricSelect.value;
  renderActionPanel();
});
actionEnvSelect?.addEventListener('change', () => {
  currentActionEnv = actionEnvSelect.value;
  loadActionTrace(true);
});
actionPointsSelect?.addEventListener('change', () => {
  currentActionPoints = Number(actionPointsSelect.value) || 1500;
  loadActionTrace(true);
});

loadInsights();

async function loadInsights() {
  try {
    const res = await fetch('/api/experiment-details');
    if (!res.ok) throw new Error('failed');
    const payload = await res.json();
    const runs = payload.runs ?? [];
    const jobs = payload.jobs ?? [];
    currentRuns = runs;
    jobLookup = buildJobLookup(jobs);
    updateSummary(runs, selectedRunId);
    renderTable(runs);
    renderCharts(runs);
    if (selectedRunId) {
      const match = runs.find((run) => run.name === selectedRunId);
      if (match) {
        selectRun(match);
      } else {
        clearDetailPanel();
      }
    }
  } catch (err) {
    console.error('Failed to load run insights', err);
  }
}

function buildJobLookup(jobs) {
  const map = new Map();
  jobs.forEach((job) => {
    const runDir = job?.result?.run_dir;
    if (runDir) {
      map.set(runDir, job);
    }
  });
  return map;
}

function updateSummary(runs, selectedId) {
  if (!runs.length) {
    bestRewardEl.textContent = '—';
    bestRewardTagEl.textContent = 'No runs yet';
    selectedRewardEl.textContent = '—';
    selectedLabelEl.textContent = 'Click a run below to analyze';
    latestRunEl.textContent = '—';
    latestRunTimeEl.textContent = '—';
    avgStepsEl.textContent = '—';
    avgFpsEl.textContent = '—';
    return;
  }
  const best = [...runs]
    .filter((run) => typeof run.eval_summary?.mean_reward === 'number')
    .sort((a, b) => b.eval_summary.mean_reward - a.eval_summary.mean_reward)[0];
  if (best) {
    bestRewardEl.textContent = formatNumber(best.eval_summary.mean_reward);
    bestRewardTagEl.textContent = best.tag || best.name;
  }
  const latest = runs[0];
  const selected = selectedId ? runs.find((run) => run.name === selectedId) : null;
  const selectedMean = selected?.eval_summary?.mean_reward;
  selectedRewardEl.textContent = selectedMean === undefined ? '—' : formatNumber(selectedMean);
  if (selected) {
    const profit = selected.eval_summary?.mean_profit_usd;
    const labelParts = [selected.tag || selected.name];
    if (profit !== undefined) {
      labelParts.push(formatCurrency(profit));
    }
    selectedLabelEl.textContent = labelParts.join(' • ');
  } else {
    selectedLabelEl.textContent = 'Click a run below to analyze';
  }
  latestRunEl.textContent = selected ? selected.name : latest.name;
  latestRunTimeEl.textContent = formatDate((selected ?? latest).created_at);
  const steps = runs
    .map((run) => run.train_meta?.total_timesteps ?? 0)
    .filter((val) => typeof val === 'number' && val > 0);
  if (steps.length) {
    const avg = steps.reduce((a, b) => a + b, 0) / steps.length;
    avgStepsEl.textContent = Number(avg).toLocaleString(undefined, { maximumFractionDigits: 0 });
  } else {
    avgStepsEl.textContent = '—';
  }
  const fpsValues = runs
    .map((run) => {
      const job = jobLookup.get(run.run_dir || '');
      const secs = job?.duration_seconds;
      const ts = run.train_meta?.total_timesteps;
      if (!secs || !ts) return null;
      return ts / secs;
    })
    .filter((val) => typeof val === 'number' && Number.isFinite(val));
  if (fpsValues.length) {
    const avgFps = fpsValues.reduce((a, b) => a + b, 0) / fpsValues.length;
    avgFpsEl.textContent = `${avgFps.toFixed(1)} fps`; 
  } else {
    avgFpsEl.textContent = '—';
  }
}

function renderTable(runs) {
  runsTableBody.innerHTML = '';
  runs.forEach((run) => {
    const row = document.createElement('tr');
    const mean = run.eval_summary?.mean_reward;
    const meanProfit = run.eval_summary?.mean_profit_usd;
    const std = run.eval_summary?.std_reward ?? run.eval_summary?.std ?? '—';
    row.innerHTML = `
      <td>${run.name}</td>
      <td>${run.tag}</td>
      <td>${mean === undefined ? '—' : formatNumber(mean)}</td>
      <td>${meanProfit === undefined ? '—' : formatCurrency(meanProfit)}</td>
      <td>${std === undefined ? '—' : formatNumber(std)}</td>
      <td>${(run.train_meta?.total_timesteps ?? '—').toLocaleString?.() || run.train_meta?.total_timesteps || '—'}</td>
      <td>${run.train_meta?.seed ?? '—'}</td>
      <td>${formatDate(run.created_at)}</td>
    `;
    row.dataset.runName = run.name;
    row.addEventListener('click', () => selectRun(run));
    runsTableBody.appendChild(row);
  });
}

function renderCharts(runs) {
  const labels = runs.map((run) => run.tag || run.name);
  const rewardMetric = rewardMetricSelect?.value || 'mean_reward';
  const rewards = runs.map((run) => selectRewardMetric(run, rewardMetric));
  const throughputMetric = throughputMetricSelect?.value || 'total_timesteps';
  const throughputData = runs.map((run) => selectThroughputMetric(run, throughputMetric));
  const selectedIndex = selectedRunId ? runs.findIndex((run) => run.name === selectedRunId) : -1;

  if (rewardChart) rewardChart.destroy();
  rewardChart = new Chart(rewardCanvas, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: rewardMetricLabel(rewardMetric),
          data: rewards,
          borderColor: '#ff8a5c',
          backgroundColor: 'rgba(255,138,92,0.2)',
          tension: 0.3,
          spanGaps: true,
          pointBackgroundColor: rewards.map((_, idx) => (idx === selectedIndex ? '#ffd166' : '#ff8a5c')),
          pointRadius: rewards.map((_, idx) => (idx === selectedIndex ? 5 : 3)),
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
      },
      scales: {
        x: { ticks: { maxRotation: 45, minRotation: 45 } },
        y: { beginAtZero: false },
      },
    },
  });

  if (throughputChart) throughputChart.destroy();
  throughputChart = new Chart(throughputCanvas, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: throughputMetricLabel(throughputMetric),
          data: throughputData,
          backgroundColor: throughputData.map((_, idx) => (idx === selectedIndex ? 'rgba(255, 214, 102, 0.8)' : 'rgba(92, 201, 255, 0.6)')),
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: (value) => {
              if (value >= 1_000_000) return `${value / 1_000_000}M`;
              if (value >= 1_000) return `${value / 1_000}K`;
              return value;
            },
          },
        },
      },
    },
  });

  const scatterData = runs
    .map((run) => {
      const job = jobLookup.get(run.run_dir || '');
      const duration = job?.duration_seconds;
      const reward = run.eval_summary?.mean_reward;
      if (!duration || reward === undefined) return null;
      const fps = run.train_meta?.total_timesteps && duration ? run.train_meta.total_timesteps / duration : null;
      const profit = run.eval_summary?.mean_profit_usd;
      return {x: duration, y: reward, label: run.tag || run.name, fps, profit, idx: run.name};
    })
    .filter(Boolean);
  if (scatterChart) scatterChart.destroy();
  scatterChart = new Chart(scatterCanvas, {
    type: 'scatter',
    data: {
      datasets: [
        {
          label: 'Reward vs Duration',
          data: scatterData,
          backgroundColor: scatterData.map((point) => (point.idx === selectedRunId ? '#ffd166' : '#5cc9ff')),
        },
      ],
    },
    options: {
      plugins: {
        tooltip: {
          callbacks: {
            label(context) {
              const point = context.raw;
              const label = point.label;
              const duration = formatDuration(point.x);
              const reward = formatNumber(point.y);
              const fps = point.fps ? `${point.fps.toFixed(1)} fps` : '—';
              const profit = point.profit !== undefined ? formatCurrency(point.profit) : '—';
              return `${label}: reward ${reward}, duration ${duration}, ${fps}, profit ${profit}`;
            },
          },
        },
        legend: { display: false },
      },
      scales: {
        x: {
          title: { display: true, text: 'Duration (seconds)' },
        },
        y: {
          title: { display: true, text: 'Mean Reward' },
        },
      },
    },
  });
}

function formatMetricValue(value, metric) {
  if (value === null || value === undefined || Number.isNaN(value)) return '—';
  if (metric === 'drawdown') return formatPercent(value);
  if (metric === 'equity' || metric === 'cash' || metric === 'episode_pnl_usd' || metric === 'last_price') {
    return formatCurrency(value);
  }
  return formatNumber(value);
}

function formatNumber(value, maxDigits = 3) {
  if (value === null || value === undefined || Number.isNaN(value)) return '—';
  return Number(value).toLocaleString(undefined, { maximumFractionDigits: maxDigits });
}

function formatCurrency(value) {
  if (value === null || value === undefined || Number.isNaN(value)) return '—';
  return currencyFormatter.format(Number(value));
}

function formatPercent(value) {
  if (value === null || value === undefined || Number.isNaN(value)) return '—';
  return `${(Number(value) * 100).toFixed(2)}%`;
}

function formatDate(value) {
  if (!value) return '—';
  return new Date(value).toLocaleString();
}

function selectRewardMetric(run, metric) {
  if (metric === 'std_reward') {
    return run.eval_summary?.std_reward ?? run.eval_summary?.std ?? null;
  }
  if (metric === 'eval_episodes') {
    return run.train_meta?.eval_episodes ?? run.eval_summary?.episodes ?? null;
  }
  if (metric === 'mean_profit_usd') {
    return run.eval_summary?.mean_profit_usd ?? null;
  }
  return run.eval_summary?.mean_reward ?? null;
}

function selectThroughputMetric(run, metric) {
  if (metric === 'duration_seconds') {
    const job = jobLookup.get(run.run_dir || '');
    return job?.duration_seconds ?? null;
  }
  if (metric === 'fps') {
    const job = jobLookup.get(run.run_dir || '');
    const duration = job?.duration_seconds;
    const steps = run.train_meta?.total_timesteps;
    if (!duration || !steps) return null;
    return steps / duration;
  }
  return run.train_meta?.total_timesteps ?? null;
}

function rewardMetricLabel(metric) {
  if (metric === 'std_reward') return 'Std Reward';
  if (metric === 'eval_episodes') return 'Eval Episodes';
  if (metric === 'mean_profit_usd') return 'Mean PnL ($)';
  return 'Mean Reward';
}

function throughputMetricLabel(metric) {
  if (metric === 'duration_seconds') return 'Duration (s)';
  if (metric === 'fps') return 'Avg FPS';
  return 'Total Timesteps';
}

function selectRun(run) {
  selectedRunId = run.name;
  runsTableBody.querySelectorAll('tr').forEach((row) => {
    row.classList.toggle('selected', row.dataset.runName === run.name);
  });
  const job = jobLookup.get(run.run_dir || '');
  updateDetailPanel(run, job);
  updateSummary(currentRuns, selectedRunId);
  renderCharts(currentRuns);
  if (actionEnvSelect) {
    currentActionEnv = 'all';
    actionEnvSelect.value = 'all';
  }
  actionMetricSelect && (currentActionMetric = actionMetricSelect.value || 'equity');
  loadActionTrace(true);
}

function updateDetailPanel(run, job) {
  if (!run) {
    clearDetailPanel();
    return;
  }
  detailPanel.hidden = false;
  detailRunLabel.textContent = run.name;
  detailTag.textContent = run.tag || run.name;
  detailStatus.textContent = job?.status || 'unknown';
  const duration = job?.duration_seconds;
  if (duration !== undefined) {
    detailDuration.textContent = formatDuration(duration);
    detailDurationExact.textContent = `${Number(duration).toFixed(1)} seconds`;
  } else {
    detailDuration.textContent = '—';
    detailDurationExact.textContent = '';
  }
  const fps = run.train_meta?.total_timesteps && duration ? run.train_meta.total_timesteps / duration : null;
  detailFps.textContent = fps ? `${fps.toFixed(1)} fps` : '—';
  const profit = run.eval_summary?.mean_profit_usd;
  detailProfit.textContent = profit === undefined ? '—' : formatCurrency(profit);
  const returnPct = run.eval_summary?.mean_return_pct;
  detailReturn.textContent = returnPct === undefined ? '—' : `${(returnPct * 100).toFixed(2)}% mean return`;
  const seed = job?.seed ?? run.train_meta?.seed;
  detailSeed.textContent = seed ?? '—';
  const episodes = job?.episodes ?? run.train_meta?.eval_episodes;
  detailEpisodes.textContent = episodes ? `${episodes} eval episodes` : '—';
  detailEnv.textContent = job?.env_config_path || run.train_meta?.env_config_path || '—';
  detailTrain.textContent = job?.train_config_path || '—';
  detailRunDir.textContent = job?.result?.run_dir || run.run_dir || '—';
  detailOverrides.textContent = JSON.stringify(job?.overrides || {}, null, 2);
}

function clearDetailPanel() {
  detailPanel.hidden = true;
  selectedRunId = null;
  runsTableBody.querySelectorAll('tr').forEach((row) => row.classList.remove('selected'));
  if (actionsPanel) {
    actionsPanel.hidden = true;
  }
  currentActionData = null;
}

async function loadActionTrace(force = false) {
  if (!actionsPanel) return;
  if (!selectedRunId) {
    actionsPanel.hidden = true;
    return;
  }
  const envValue = currentActionEnv ?? 'all';
  const points = Number(currentActionPoints) || 1500;
  const cacheKey = `${selectedRunId}::${envValue}::${points}`;
  if (!force && actionCache.has(cacheKey)) {
    currentActionData = actionCache.get(cacheKey);
    syncActionSelectors(currentActionData, envValue);
    renderActionPanel();
    return;
  }
  actionsPanel.hidden = false;
  actionSummaryEl.textContent = 'Loading action log…';
  const params = new URLSearchParams();
  params.set('max_points', points);
  ACTION_METRICS.forEach((metric) => params.append('metrics', metric));
  if (envValue !== 'all') {
    params.set('env_index', envValue);
  }
  try {
    const res = await fetch(`/api/run-actions/${encodeURIComponent(selectedRunId)}?${params.toString()}`);
    if (!res.ok) throw new Error('Request failed');
    const payload = await res.json();
    actionCache.set(cacheKey, payload);
    currentActionData = payload;
    syncActionSelectors(payload, envValue);
    renderActionPanel();
  } catch (err) {
    console.error('Failed to load action log', err);
    currentActionData = null;
    actionSummaryEl.textContent = 'Unable to load action log for this run.';
    renderActionPanel();
  }
}

function syncActionSelectors(payload, envValue) {
  if (actionEnvSelect) {
    const nextOptions = ['all'];
    const envCount = payload?.env_count ?? 0;
    for (let i = 0; i < envCount; i += 1) {
      nextOptions.push(String(i));
    }
    actionEnvSelect.innerHTML = '';
    nextOptions.forEach((value) => {
      const option = document.createElement('option');
      option.value = value;
      option.textContent = value === 'all' ? 'All' : `Env ${value}`;
      if (value === envValue) option.selected = true;
      actionEnvSelect.appendChild(option);
    });
  }
  if (actionPointsSelect) {
    actionPointsSelect.value = String(Number(currentActionPoints) || 1500);
  }
  if (actionMetricSelect && payload) {
    const metrics = (payload.available_metrics || []).filter((metric) => payload.series?.[metric]);
    actionMetricSelect.innerHTML = '';
    if (!metrics.length) {
      const opt = document.createElement('option');
      opt.value = '';
      opt.textContent = 'No metrics available';
      actionMetricSelect.appendChild(opt);
      currentActionMetric = '';
      return;
    }
    if (!metrics.includes(currentActionMetric)) {
      currentActionMetric = metrics[0];
    }
    metrics.forEach((metric) => {
      const option = document.createElement('option');
      option.value = metric;
      option.textContent = ACTION_METRIC_LABELS[metric] || metric;
      if (metric === currentActionMetric) option.selected = true;
      actionMetricSelect.appendChild(option);
    });
  }
}

function renderActionPanel() {
  if (!actionsPanel) return;
  if (!currentActionData || !currentActionMetric) {
    actionsPanel.hidden = !selectedRunId;
    if (actionChart) {
      actionChart.destroy();
      actionChart = null;
    }
    return;
  }
  actionsPanel.hidden = false;
  const series = currentActionData.series?.[currentActionMetric];
  const points = series?.points ?? [];
  const metricLabel = ACTION_METRIC_LABELS[currentActionMetric] || currentActionMetric;
  if (!points.length) {
    if (actionChart) {
      actionChart.destroy();
      actionChart = null;
    }
    actionSummaryEl.textContent = `No ${metricLabel} samples for this selection.`;
  } else if (actionChartCanvas) {
    actionSummaryEl.textContent = `${currentActionData.filtered_rows?.toLocaleString?.() || currentActionData.filtered_rows} rows from ${currentActionData.action_log_path}`;
    const labels = points.map((point) => point.step);
    const values = points.map((point) => point.value);
    if (actionChart) actionChart.destroy();
    actionChart = new Chart(actionChartCanvas, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: metricLabel,
            data: values,
            borderColor: metricColor(currentActionMetric),
            backgroundColor: 'rgba(92,201,255,0.2)',
            pointRadius: 0,
            tension: 0.15,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { title: { display: true, text: 'Global Step' } },
          y: { title: { display: true, text: metricLabel } },
        },
      },
    });
  }
  actionStatStart.textContent = formatMetricValue(series?.start, currentActionMetric);
  actionStatEnd.textContent = formatMetricValue(series?.end, currentActionMetric);
  const minText = formatMetricValue(series?.min, currentActionMetric);
  const maxText = formatMetricValue(series?.max, currentActionMetric);
  actionStatMinMax.textContent = series ? `${minText} / ${maxText}` : '—';
  actionStatMean.textContent = formatMetricValue(series?.mean, currentActionMetric);
  const filtered = currentActionData.filtered_rows ?? 0;
  const total = currentActionData.total_rows ?? filtered;
  actionStatRows.textContent = `${filtered.toLocaleString()} / ${total.toLocaleString()} rows`;
  actionLogPathEl.textContent = currentActionData.action_log_path || '—';
  renderActionSampleTable(currentActionData.sample_rows || []);
}

function renderActionSampleTable(rows) {
  if (!actionSampleBody) return;
  actionSampleBody.innerHTML = '';
  if (!rows.length) {
    const emptyRow = document.createElement('tr');
    emptyRow.innerHTML = `<td colspan="11">No sample rows available.</td>`;
    actionSampleBody.appendChild(emptyRow);
    return;
  }
  rows.forEach((row) => {
    const tr = document.createElement('tr');
    tr.innerHTML = ACTION_SAMPLE_FIELDS.map((field) => `<td>${formatSampleField(field, row[field])}</td>`).join('');
    actionSampleBody.appendChild(tr);
  });
}

function formatSampleField(field, value) {
  if (value === null || value === undefined || Number.isNaN(value)) return '—';
  if (field === 'cash' || field === 'equity' || field === 'episode_pnl_usd') {
    return formatCurrency(value);
  }
  if (field === 'drawdown') {
    return formatPercent(value);
  }
  if (typeof value === 'number') {
    return formatNumber(value);
  }
  return String(value);
}

function metricColor(metric) {
  if (metric === 'equity' || metric === 'cash') return '#5cc9ff';
  if (metric === 'drawdown') return '#ff8a5c';
  if (metric === 'episode_pnl_usd') return '#ffd166';
  if (metric === 'position' || metric === 'target_position') return '#a78bfa';
  return '#90f48b';
}

function formatDuration(seconds) {
  if (!seconds && seconds !== 0) {
    return '—';
  }
  if (seconds < 60) {
    return `${seconds.toFixed(1)}s`;
  }
  const minutes = seconds / 60;
  if (minutes < 60) {
    return `${minutes.toFixed(1)}m`;
  }
  const hours = minutes / 60;
  return `${hours.toFixed(1)}h`;
}
