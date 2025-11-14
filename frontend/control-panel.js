const form = document.getElementById('experimentForm');
const envSelect = document.getElementById('envConfig');
const trainingSelect = document.getElementById('trainingConfig');
const manifestSelect = document.getElementById('indicatorManifest');
const riskInput = document.getElementById('riskPct');
const stopStepsInput = document.getElementById('stopLossSteps');
const limitFeeInput = document.getElementById('limitFeeBps');
const marketFeeInput = document.getElementById('marketFeeBps');
const episodesInput = document.getElementById('episodes');
const seedInput = document.getElementById('seed');
const tagInput = document.getElementById('tag');
const datasetTableBody = document.querySelector('#datasetTable tbody');
const indicatorCatalogEl = document.getElementById('indicatorCatalog');
const clearIndicatorsBtn = document.getElementById('clearIndicators');
const jobsTableBody = document.querySelector('#jobsTable tbody');
const runsTableBody = document.querySelector('#runsTable tbody');
const refreshJobsBtn = document.getElementById('refreshJobs');
const refreshRunsBtn = document.getElementById('refreshRuns');

const API_BASE = '/api';
const jobPollers = new Map();
let runOptions = null;

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const payload = buildPayload();
  try {
    const response = await fetch(`${API_BASE}/experiment-jobs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(err.detail || response.statusText);
    }
    const job = await response.json();
    upsertJob(job);
    startPolling(job.id);
  } catch (err) {
    alert(`Failed to launch run: ${err.message}`);
  }
});

manifestSelect.addEventListener('change', () => handleManifestModeChange());
refreshJobsBtn.addEventListener('click', () => loadJobs());
refreshRunsBtn.addEventListener('click', () => loadRuns());
clearIndicatorsBtn?.addEventListener('click', () => clearIndicatorSelections());

function buildPayload() {
  const payload = {
    env_config_path: envSelect.value,
    train_config_path: trainingSelect.value,
    indicator_manifest_path: manifestSelect.value || null,
    tag: tagInput.value.trim() || 'control-panel',
    episodes: parseInt(episodesInput.value, 10) || 1,
    seed: parseInt(seedInput.value, 10) || 0
  };

  const numericFields = [
    ['risk_pct', parseFloat(riskInput.value)],
    ['stop_loss_steps', parseInt(stopStepsInput.value, 10)],
    ['limit_fee_pct', parseFloat(limitFeeInput.value)],
    ['market_fee_pct', parseFloat(marketFeeInput.value)]
  ];
  for (const [key, value] of numericFields) {
    if (!Number.isNaN(value) && value !== null) {
      payload[key] = value;
    }
  }
  const manifestPath = manifestSelect.value;
  if (manifestPath) {
    payload.indicator_manifest_path = manifestPath;
  } else {
    const customIndicators = collectSelectedIndicators();
    if (customIndicators.length) {
      payload.indicator_manifest_inline = customIndicators;
    }
  }
  return payload;
}

async function loadOptions() {
  try {
    const res = await fetch(`${API_BASE}/run-options`);
    if (!res.ok) throw new Error('options fetch failed');
    runOptions = await res.json();
    populateSelects();
    applyEnvDefaults();
  } catch (err) {
    console.error('Failed to load run options', err);
  }
}

function populateSelects() {
  populateSelect(envSelect, runOptions?.env_configs ?? []);
  populateSelect(
    trainingSelect,
    runOptions?.training_configs ?? [],
    false,
    formatTrainingOptionLabel,
  );
  populateSelect(manifestSelect, runOptions?.indicator_manifests ?? [], true);
  renderIndicatorCatalog();
}

function populateSelect(select, items, allowEmpty = false, formatter = null) {
  select.innerHTML = '';
  if (allowEmpty) {
    const opt = document.createElement('option');
    opt.value = '';
    opt.textContent = 'Custom mix (select below)';
    select.appendChild(opt);
  }
  for (const item of items) {
    const option = document.createElement('option');
    option.value = item.path;
    option.textContent = formatter ? formatter(item) : (item.name || item.path);
    select.appendChild(option);
  }
}

function formatTrainingOptionLabel(config) {
  const name = config.name || config.path;
  const algo = (config.algorithm || '').toUpperCase();
  const steps = typeof config.total_timesteps === 'number' ? config.total_timesteps.toLocaleString() : '—';
  const device = config.device || 'cpu';
  const envs = config.num_envs ? `${config.num_envs} envs` : '1 env';
  return `${name} [${algo || 'N/A'} | ${steps} steps | ${device} | ${envs}]`;
}

function applyEnvDefaults() {
  if (!runOptions?.env_configs?.length) return;
  const selected = runOptions.env_configs[0];
  envSelect.value = selected.path;
  if (selected.risk_pct !== undefined) riskInput.value = selected.risk_pct;
  if (selected.stop_loss_steps !== undefined) stopStepsInput.value = selected.stop_loss_steps;
  if (selected.limit_fee_bps !== undefined) limitFeeInput.value = (selected.limit_fee_bps / 100).toFixed(3);
  if (selected.market_fee_bps !== undefined) marketFeeInput.value = (selected.market_fee_bps / 100).toFixed(3);
  if (selected.indicator_manifest_path) {
    manifestSelect.value = selected.indicator_manifest_path;
  }
  if (runOptions.training_configs?.length) {
    trainingSelect.value = runOptions.training_configs[0].path;
  }
  handleManifestModeChange();
}

async function loadJobs() {
  try {
    const res = await fetch(`${API_BASE}/experiment-jobs`);
    if (!res.ok) throw new Error('failed to fetch jobs');
    const jobs = await res.json();
    jobsTableBody.innerHTML = '';
    for (const job of jobs) {
      upsertJob(job);
      if (job.status === 'queued' || job.status === 'running') {
        startPolling(job.id);
      }
    }
  } catch (err) {
    console.error('Failed to load jobs', err);
  }
}

async function loadRuns() {
  try {
    const res = await fetch(`${API_BASE}/experiment-runs`);
    if (!res.ok) throw new Error('runs fetch failed');
    const runs = await res.json();
    runsTableBody.innerHTML = '';
    for (const run of runs) {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${run.name}</td>
        <td>${run.tag}</td>
        <td>${formatNumber(run.eval_summary?.mean_reward)}</td>
        <td>${run.train_meta?.total_timesteps ?? '—'}</td>
        <td>${formatDate(run.created_at)}</td>
      `;
      runsTableBody.appendChild(row);
    }
  } catch (err) {
    console.error('Failed to load runs', err);
  }
}

function upsertJob(job) {
  let row = document.querySelector(`tr[data-job-id="${job.id}"]`);
  if (!row) {
    row = document.createElement('tr');
    row.dataset.jobId = job.id;
    row.innerHTML = '<td class="id"></td><td class="tag"></td><td class="status"></td><td class="episodes"></td><td class="seed"></td><td class="result"></td><td class="updated"></td>';
    jobsTableBody.appendChild(row);
  }
  row.querySelector('.id').textContent = job.id.slice(0, 8);
  row.querySelector('.tag').textContent = job.tag;
  row.querySelector('.status').textContent = job.status;
  row.querySelector('.episodes').textContent = job.episodes;
  row.querySelector('.seed').textContent = job.seed;
  row.querySelector('.result').textContent = summarizeResult(job);
  row.querySelector('.updated').textContent = formatDate(job.updated_at);
}

function summarizeResult(job) {
  if (job.status === 'failed') {
    return job.error || 'failed';
  }
  if (job.result?.mean_reward !== undefined) {
    return `mean ${formatNumber(job.result.mean_reward)}`;
  }
  if (job.result?.run_dir) {
    return job.result.run_dir;
  }
  return job.status === 'completed' ? 'done' : '—';
}

function startPolling(jobId) {
  if (jobPollers.has(jobId)) return;
  const interval = setInterval(async () => {
    try {
      const res = await fetch(`${API_BASE}/experiment-jobs/${jobId}`);
      if (!res.ok) throw new Error('job fetch failed');
      const job = await res.json();
      upsertJob(job);
      if (job.status === 'completed' || job.status === 'failed') {
        clearInterval(interval);
        jobPollers.delete(jobId);
        loadRuns();
      }
    } catch (err) {
      console.warn('Polling failed', err);
      clearInterval(interval);
      jobPollers.delete(jobId);
    }
  }, 5000);
  jobPollers.set(jobId, interval);
}

function formatDate(value) {
  if (!value) return '—';
  return new Date(value).toLocaleString();
}

function formatNumber(value) {
  if (value === null || value === undefined) return '—';
  return Number(value).toFixed(4);
}

loadOptions();
loadJobs();
loadRuns();
loadDatasets();

function renderIndicatorCatalog() {
  if (!indicatorCatalogEl) return;
  indicatorCatalogEl.innerHTML = '';
  const catalog = runOptions?.indicator_catalog ?? [];
  catalog.forEach((spec) => {
    const card = document.createElement('div');
    card.className = 'indicator-card';
    card.dataset.indicator = spec.name;

    const header = document.createElement('label');
    header.className = 'indicator-header';
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.dataset.role = 'toggle';
    checkbox.dataset.indicator = spec.name;
    checkbox.addEventListener('change', () => updateIndicatorDisabledState(card));
    header.appendChild(checkbox);

    const title = document.createElement('span');
    title.textContent = spec.label || spec.name;
    header.appendChild(title);
    card.appendChild(header);

    if (spec.description) {
      const desc = document.createElement('p');
      desc.className = 'indicator-desc';
      desc.textContent = spec.description;
      card.appendChild(desc);
    }

    if (spec.params?.length) {
      const paramsContainer = document.createElement('div');
      paramsContainer.className = 'indicator-params';
      spec.params.forEach((param) => {
        const paramLabel = document.createElement('label');
        paramLabel.textContent = param.label;
        const input = buildParamInput(param);
        input.dataset.param = param.key;
        input.dataset.type = param.type;
        input.disabled = true;
        paramLabel.appendChild(input);
        paramsContainer.appendChild(paramLabel);
      });
      card.appendChild(paramsContainer);
    }

    indicatorCatalogEl.appendChild(card);
  });
  handleManifestModeChange();
}

function buildParamInput(param) {
  let input;
  if (param.type === 'choice') {
    input = document.createElement('select');
    (param.options || []).forEach((opt) => {
      const option = document.createElement('option');
      option.value = opt;
      option.textContent = opt;
      input.appendChild(option);
    });
    input.value = param.default ?? (param.options?.[0] ?? '');
  } else {
    input = document.createElement('input');
    input.type = 'number';
    input.step = param.step ?? (param.type === 'int' ? 1 : 0.1);
    if (param.min !== undefined) input.min = param.min;
    if (param.max !== undefined) input.max = param.max;
    input.value = param.default ?? 0;
  }
  input.dataset.default = param.default ?? '';
  if (param.type === 'int' || param.type === 'float') {
    input.dataset.type = param.type;
  }
  return input;
}

function collectSelectedIndicators() {
  if (!indicatorCatalogEl) return [];
  const selections = [];
  indicatorCatalogEl.querySelectorAll('.indicator-card').forEach((card) => {
    const toggle = card.querySelector('input[type="checkbox"][data-role="toggle"]');
    if (!toggle || !toggle.checked) return;
    const params = {};
    card.querySelectorAll('[data-param]').forEach((input) => {
      if (input.disabled) return;
      const type = input.dataset.type;
      params[input.dataset.param] = coerceParamValue(input, type);
    });
    selections.push({
      name: card.dataset.indicator,
      params,
    });
  });
  return selections;
}

function updateIndicatorDisabledState(card) {
  const toggle = card.querySelector('input[type="checkbox"][data-role="toggle"]');
  const disabled = manifestSelect.value !== '' || !toggle.checked;
  card.querySelectorAll('[data-param]').forEach((input) => {
    input.disabled = disabled;
  });
  if (manifestSelect.value !== '') {
    card.classList.add('disabled');
  } else {
    card.classList.toggle('disabled', !toggle.checked);
  }
}

function handleManifestModeChange() {
  const usePreset = manifestSelect.value !== '';
  if (clearIndicatorsBtn) clearIndicatorsBtn.disabled = usePreset;
  if (!indicatorCatalogEl) return;
  indicatorCatalogEl.classList.toggle('disabled', usePreset);
  indicatorCatalogEl.querySelectorAll('.indicator-card').forEach((card) => {
    if (usePreset) {
      const toggle = card.querySelector('input[type="checkbox"][data-role="toggle"]');
      if (toggle) toggle.checked = false;
      card.querySelectorAll('[data-param]').forEach((input) => {
        input.disabled = true;
      });
      card.classList.add('disabled');
    } else {
      card.classList.remove('disabled');
      updateIndicatorDisabledState(card);
    }
  });
}

function clearIndicatorSelections() {
  if (!indicatorCatalogEl) return;
  indicatorCatalogEl.querySelectorAll('input[type="checkbox"][data-role="toggle"]').forEach((toggle) => {
    toggle.checked = false;
  });
  indicatorCatalogEl.querySelectorAll('[data-param]').forEach((input) => {
    input.disabled = true;
  });
  indicatorCatalogEl.querySelectorAll('.indicator-card').forEach((card) => {
    card.classList.add('disabled');
  });
}

function coerceParamValue(input, type) {
  if (type === 'choice') {
    return input.value;
  }
  if (type === 'int') {
    let parsed = parseInt(input.value, 10);
    if (Number.isNaN(parsed)) {
      parsed = parseInt(input.dataset.default ?? '0', 10) || 0;
    }
    return parsed;
  }
  if (type === 'float') {
    let parsed = parseFloat(input.value);
    if (Number.isNaN(parsed)) {
      parsed = parseFloat(input.dataset.default ?? '0') || 0;
    }
    return parsed;
  }
  return input.value;
}

async function loadDatasets() {
  if (!datasetTableBody) return;
  try {
    const res = await fetch(`${API_BASE}/dataset-manifests`);
    if (!res.ok) throw new Error('dataset fetch failed');
    const manifests = await res.json();
    datasetTableBody.innerHTML = '';
    manifests.sort((a, b) => new Date(a.start_ts) - new Date(b.start_ts));
    for (const manifest of manifests) {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${manifest.name}</td>
        <td>${manifest.symbol} (${manifest.timeframe})</td>
        <td>${formatDate(manifest.start_ts)} &rarr; ${formatDate(manifest.end_ts)}</td>
        <td>${manifest.total_rows.toLocaleString()}</td>
      `;
      datasetTableBody.appendChild(row);
    }
  } catch (err) {
    console.error('Failed to load dataset manifests', err);
  }
}
