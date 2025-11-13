const form = document.getElementById('fetchForm');
const jobsTableBody = document.querySelector('#jobsTable tbody');
const coverageTableBody = document.querySelector('#coverageTable tbody');
const coverageSymbol = document.getElementById('coverageSymbol');
const refreshCoverageBtn = document.getElementById('refreshCoverage');

const API_BASE = '/api';
const jobPollers = new Map();

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const payload = buildPayload();
  const response = await fetch(`${API_BASE}/data-jobs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!response.ok) {
    const err = await response.json();
    alert(`Failed to create job: ${err.detail || response.statusText}`);
    return;
  }
  const job = await response.json();
  addOrUpdateJob(job);
  startPolling(job.id);
});

refreshCoverageBtn.addEventListener('click', () => loadCoverage());
coverageSymbol.addEventListener('change', () => loadCoverage());

function buildPayload() {
  const start = document.getElementById('start').value;
  const end = document.getElementById('end').value;
  return {
    exchange: document.getElementById('exchange').value,
    symbol: document.getElementById('symbol').value,
    timeframe: document.getElementById('timeframe').value,
    start_timestamp: start ? new Date(start).toISOString() : null,
    end_timestamp: end ? new Date(end).toISOString() : null,
    options: {
      full_history: document.getElementById('fullHistory').checked
    }
  };
}

async function fetchJob(jobId) {
  const response = await fetch(`${API_BASE}/data-jobs/${jobId}`);
  if (!response.ok) throw new Error('Job not found');
  return response.json();
}

function addOrUpdateJob(job) {
  let row = document.querySelector(`tr[data-job-id="${job.id}"]`);
  if (!row) {
    row = document.createElement('tr');
    row.dataset.jobId = job.id;
    row.innerHTML = '<td class="id"></td><td class="symbol"></td><td class="tf"></td><td class="status"></td><td class="progress"></td><td class="updated"></td><td class="info"></td>';
    jobsTableBody.prepend(row);
  }
  row.querySelector('.id').textContent = job.id.slice(0, 8);
  row.querySelector('.symbol').textContent = job.symbol;
  row.querySelector('.tf').textContent = job.timeframe;
  row.querySelector('.status').textContent = job.status;
  row.querySelector('.progress').textContent = `${Math.round(job.progress * 100)}%`;
  row.querySelector('.updated').textContent = new Date(job.updated_at).toLocaleString();
  const info = job.details?.error || job.details?.zip_error || '';
  row.querySelector('.info').textContent = info;
  row.querySelector('.info').title = info;
}

function startPolling(jobId) {
  if (jobPollers.has(jobId)) return;
  const interval = setInterval(async () => {
    try {
      const job = await fetchJob(jobId);
      addOrUpdateJob(job);
      if (job.status === 'completed' || job.status === 'failed') {
        clearInterval(interval);
        jobPollers.delete(jobId);
        loadCoverage();
      }
    } catch (err) {
      console.error('Polling failed', err);
      clearInterval(interval);
      jobPollers.delete(jobId);
    }
  }, 4000);
  jobPollers.set(jobId, interval);
}

async function loadCoverage() {
  const symbol = coverageSymbol.value;
  const response = await fetch(`${API_BASE}/data-coverage?exchange=kraken&symbol=${encodeURIComponent(symbol)}`);
  if (!response.ok) {
    console.warn('Coverage fetch failed');
    return;
  }
  const entries = await response.json();
  coverageTableBody.innerHTML = '';
  entries.sort((a, b) => a.timeframe.localeCompare(b.timeframe));
  for (const entry of entries) {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${entry.timeframe}</td>
      <td>${formatTs(entry.start_timestamp)}</td>
      <td>${formatTs(entry.end_timestamp)}</td>
    `;
    coverageTableBody.appendChild(row);
  }
}

function formatTs(ts) {
  if (!ts) return '—';
  return new Date(ts).toISOString();
}

// initial
loadCoverage();
