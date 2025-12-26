const $ = (id) => document.getElementById(id);

const statusEl = $("status");
const jobsEl = $("jobs");
const matchesEl = $("matches");
const profilesSelect = $("profilesSelect");

function setStatus(msg) {
  statusEl.textContent = msg || "";
}

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`${res.status} ${res.statusText}: ${txt}`);
  }
  return res.json();
}

function renderJobs(jobs) {
  jobsEl.innerHTML = "";
  if (!jobs.length) {
    jobsEl.innerHTML = `<div class="muted">No jobs found.</div>`;
    return;
  }

  for (const j of jobs) {
    const div = document.createElement("div");
    div.className = "item";
    div.innerHTML = `
      <div class="row gap" style="justify-content:space-between">
        <div>
          <div><strong>${escapeHtml(j.title)}</strong></div>
          <div class="muted">${escapeHtml(j.location)} • ${escapeHtml(j.source)}</div>
        </div>
        <a href="${j.url}" target="_blank" rel="noreferrer">Open</a>
      </div>
      <div class="muted" style="margin-top:8px">
        ${truncate(stripHtml(j.description || ""), 220)}
      </div>
    `;
    jobsEl.appendChild(div);
  }
}

function renderProfiles(profiles) {
  profilesSelect.innerHTML = "";
  for (const p of profiles) {
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = `#${p.id} • ${p.name} (${p.role_focus}, EN ${p.english_level})`;
    profilesSelect.appendChild(opt);
  }
}

function renderMatches(items) {
  matchesEl.innerHTML = "";
  if (!items.length) {
    matchesEl.innerHTML = `<div class="muted">No matches yet. Try ingest or lower min_score.</div>`;
    return;
  }

  for (const it of items) {
    const j = it.job;
    const div = document.createElement("div");
    div.className = "item";
    div.innerHTML = `
      <div class="row gap" style="justify-content:space-between">
        <div>
          <span class="badge score">Score: ${it.score}</span>
          <strong>${escapeHtml(j.title)}</strong>
          <div class="muted">${escapeHtml(j.location)} • ${escapeHtml(j.source)}</div>
        </div>
        <a href="${j.url}" target="_blank" rel="noreferrer">Open</a>
      </div>
      <div class="muted" style="margin-top:8px">
        ${truncate(stripHtml(j.description || ""), 220)}
      </div>
    `;
    matchesEl.appendChild(div);
  }
}

async function loadJobs(q = "") {
  setStatus("Loading jobs...");
  const url = q ? `/jobs?limit=60&q=${encodeURIComponent(q)}` : `/jobs?limit=60`;
  const jobs = await api(url);
  renderJobs(jobs);
  setStatus(`Jobs loaded: ${jobs.length}`);
}

async function loadProfiles() {
  const profiles = await api("/profiles");
  renderProfiles(profiles);
}

async function runIngest() {
  setStatus("Running ingest...");
  const r = await api("/ingest", { method: "POST", body: "{}" });
  setStatus(`Ingest done: inserted=${r.inserted} sources=${r.sources}`);
  await loadJobs();
}

async function createProfile() {
  const payload = {
    name: $("pName").value.trim() || "Danny",
    role_focus: $("pRole").value.trim() || "backend_mobile",
    english_level: $("pEng").value.trim() || "B2",
    keywords: splitCsv($("pKeywords").value),
    exclude_keywords: splitCsv($("pExclude").value),
  };

  setStatus("Creating profile...");
  const p = await api("/profiles", { method: "POST", body: JSON.stringify(payload) });
  $("profileOut").textContent = JSON.stringify(p, null, 2);
  setStatus(`Profile created: id=${p.id}`);
  await loadProfiles();
}

async function loadMatches() {
  const id = Number(profilesSelect.value);
  if (!id) return;

  setStatus("Loading matches...");
  const items = await api(`/profiles/${id}/matches?min_score=30&limit=30`);
  renderMatches(items);
  setStatus(`Matches loaded: ${items.length}`);
}

function splitCsv(s) {
  return (s || "")
    .split(",")
    .map((x) => x.trim())
    .filter(Boolean);
}

function stripHtml(html) {
  return (html || "").replace(/<[^>]*>/g, " ");
}

function truncate(s, n) {
  s = (s || "").trim().replace(/\s+/g, " ");
  return s.length > n ? s.slice(0, n - 1) + "…" : s;
}

function escapeHtml(s) {
  return (s || "").replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
  }[c]));
}

// hooks
$("btnIngest").addEventListener("click", () => runIngest().catch(err => setStatus(err.message)));
$("btnReload").addEventListener("click", () => loadJobs().catch(err => setStatus(err.message)));
$("btnCreateProfile").addEventListener("click", () => createProfile().catch(err => setStatus(err.message)));
$("btnLoadMatches").addEventListener("click", () => loadMatches().catch(err => setStatus(err.message)));

$("btnSearch").addEventListener("click", () => loadJobs($("q").value).catch(err => setStatus(err.message)));
$("q").addEventListener("keydown", (e) => {
  if (e.key === "Enter") loadJobs($("q").value).catch(err => setStatus(err.message));
});

// init
(async function init() {
  try {
    await loadJobs();
    await loadProfiles();
  } catch (e) {
    setStatus(e.message);
  }
})();
