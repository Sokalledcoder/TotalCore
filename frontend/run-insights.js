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

let rewardChart;
let throughputChart;
let scatterChart;
let currentRuns = [];
let jobLookup = new Map();
let selectedRunId = null;

refreshBtn?.addEventListener('click', () => loadInsights());
rewardMetricSelect?.addEventListener('change', () => renderCharts(currentRuns));
throughputMetricSelect?.addEventListener('change', () => renderCharts(currentRuns));

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
    selectedLabelEl.textContent = selected.tag || selected.name;
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
    const std = run.eval_summary?.std_reward ?? run.eval_summary?.std ?? '—';
    row.innerHTML = `
      <td>${run.name}</td>
      <td>${run.tag}</td>
      <td>${mean === undefined ? '—' : formatNumber(mean)}</td>
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
      return {x: duration, y: reward, label: run.tag || run.name, fps, idx: run.name};
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
              return `${label}: reward ${reward}, duration ${duration}, ${fps}`;
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

function formatNumber(value) {
  if (value === null || value === undefined || Number.isNaN(value)) return '—';
  return Number(value).toFixed(3);
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
