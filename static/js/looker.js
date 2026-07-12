// ── looker.js — motor centralizado para embeds de Looker Studio ──
const LOOKER_KEYS = {};

function _key(role) { return `edusatisface_looker_${role}`; }

function autoload(role) {
  const url = localStorage.getItem(_key(role));
  if (url) _embed(role, url);
}

let _activeRole = null;

function showModal(role) {
  _activeRole = role;
  const saved = localStorage.getItem(_key(role)) || '';
  document.getElementById('lookerUrlInput').value = saved;
  document.getElementById('lookerModal').style.display = 'flex';
  setTimeout(() => document.getElementById('lookerUrlInput').focus(), 100);
}

function closeModal() {
  document.getElementById('lookerModal').style.display = 'none';
  _activeRole = null;
}

function saveAndLoad() {
  const url = document.getElementById('lookerUrlInput').value.trim();
  if (!url) { _shake('lookerUrlInput'); return; }
  localStorage.setItem(_key(_activeRole), url);
  closeModal();
  _embed(_activeRole, url);
}

function _embed(role, url) {
  const placeholder = document.getElementById(`placeholder-${role}`);
  const iframe      = document.getElementById(`iframe-${role}`);
  const status      = document.getElementById(`status-${role}`);
  const openBtn     = document.getElementById(`open-${role}`);
  if (!iframe) return;
  if (placeholder) placeholder.style.display = 'none';
  iframe.style.display = 'block';
  if (status) { status.textContent = 'Cargando...'; status.style.color = '#94A3B8'; }
  if (openBtn) { openBtn.href = url; openBtn.style.display = 'inline-flex'; }
  iframe.src = url;
}

function iframeOk(role) {
  const s = document.getElementById(`status-${role}`);
  if (s) { s.textContent = '● En vivo'; s.style.color = '#10B981'; }
}

function iframeErr(role) {
  const s = document.getElementById(`status-${role}`);
  if (s) { s.textContent = '⚠ Error al cargar'; s.style.color = '#EF4444'; }
}

function _shake(id) {
  const el = document.getElementById(id);
  el.style.animation = 'none';
  el.style.borderColor = '#EF4444';
  el.style.boxShadow = '0 0 0 3px rgba(239,68,68,.15)';
  setTimeout(() => { el.style.borderColor = ''; el.style.boxShadow = ''; }, 1500);
}

// Close modal clicking outside
document.addEventListener('click', e => {
  const modal = document.getElementById('lookerModal');
  if (modal && e.target === modal) closeModal();
});

// ESC to close
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
});
