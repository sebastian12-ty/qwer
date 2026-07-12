let allRows = [];
async function loadHistorial() {
  const data = await fetch('/api/v1/student/historial?limit=100').then(r=>r.json()).catch(()=>({rows:[]}));
  allRows = data.rows || [];
  renderTable(allRows);
  document.getElementById('historial-count').textContent = `${allRows.length} registros`;
}
function renderTable(rows) {
  const rmap = { bajo:'badge-success', medio:'badge-warning', alto:'badge-danger' };
  const smap = { positivo:'badge-success', negativo:'badge-danger', neutral:'badge-neutral' };
  const emojiM = { feliz:'😊', neutral:'😐', triste:'😢', enojado:'😠', sorprendido:'😲' };
  const stars = n => '★'.repeat(n)+'☆'.repeat(5-n);
  const tbody = document.getElementById('historialBody');
  if (!rows.length) { tbody.innerHTML='<tr><td colspan="10" style="text-align:center;padding:32px;color:#94A3B8">Sin registros</td></tr>'; return; }
  tbody.innerHTML = rows.map(r => `<tr>
    <td>${new Date(r.fecha).toLocaleDateString('es-PE')}</td>
    <td>${r.curso||'—'}</td>
    <td>${r.docente||'—'}</td>
    <td style="color:#F59E0B">${stars(r.calidad_clase||0)}</td>
    <td style="font-weight:600">${((r.indice_comprension||0)*100).toFixed(0)}%</td>
    <td style="font-weight:700;color:#4F46E5">${((r.indice_nivelacion||0)*100).toFixed(0)}%</td>
    <td>${emojiM[r.emocion_predominante]||'—'} <span style="font-size:11px">${r.emocion_predominante||'—'}</span></td>
    <td><span class="badge ${smap[r.sentimiento_label]||'badge-neutral'}">${r.sentimiento_label||'—'}</span></td>
    <td><span class="badge ${rmap[r.riesgo_insatisfaccion]||'badge-neutral'}">${r.riesgo_insatisfaccion||'—'}</span></td>
    <td><button class="btn btn-ghost btn-sm" onclick="showDetalle(${r.id})"><i class="fas fa-eye"></i></button></td>
  </tr>`).join('');
}
document.getElementById('searchInput').addEventListener('input', filter);
document.getElementById('filterRiesgo').addEventListener('change', filter);
function filter() {
  const q = document.getElementById('searchInput').value.toLowerCase();
  const r = document.getElementById('filterRiesgo').value;
  renderTable(allRows.filter(row => (!q || (row.curso||'').toLowerCase().includes(q)) && (!r || row.riesgo_insatisfaccion === r)));
}
async function showDetalle(id) {
  const r = allRows.find(x => x.id === id); if (!r) return;
  const emojiM = { feliz:'😊', neutral:'😐', triste:'😢', enojado:'😠', sorprendido:'😲' };
  const kpiBar = (label, val) => {
    const pct = ((val||0)*100).toFixed(1);
    const color = pct>=70?'#10B981':pct>=50?'#F59E0B':'#EF4444';
    return `<div style="margin-bottom:10px"><div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px"><span>${label}</span><b style="color:${color}">${pct}%</b></div><div style="background:#F1F5F9;border-radius:4px;height:6px"><div style="background:${color};height:6px;border-radius:4px;width:${pct}%"></div></div></div>`;
  };
  document.getElementById('detalleContent').innerHTML = `
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;font-size:13px">
      <div><span style="color:#64748B">Fecha:</span> <b>${new Date(r.fecha).toLocaleString('es-PE')}</b></div>
      <div><span style="color:#64748B">Emoción:</span> <b>${emojiM[r.emocion_predominante]||'—'} ${r.emocion_predominante||'—'}</b></div>
      <div><span style="color:#64748B">Calidad:</span> <b>${'★'.repeat(r.calidad_clase||0)}</b></div>
      <div><span style="color:#64748B">Sentimiento:</span> <b>${r.sentimiento_label||'—'} (${((r.sentimiento_score||0)*100).toFixed(0)}%)</b></div>
    </div>
    <div style="margin-bottom:16px">${kpiBar('Comprensión',r.indice_comprension)}${kpiBar('Atención',r.indice_atencion)}${kpiBar('Nivelación',r.indice_nivelacion)}${kpiBar('Coherencia',r.indice_coherencia_emocional)}</div>
    ${r.comentario?`<div style="background:#F8FAFC;border-radius:8px;padding:12px;font-size:12px;color:#334155"><b>💬 Comentario:</b><br>${r.comentario}</div>`:''}
    ${(r.nlp_keywords||[]).length?`<div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:4px">${(r.nlp_keywords||[]).map(k=>`<span class="chip">${k}</span>`).join('')}</div>`:''}
  `;
  document.getElementById('detalleModal').style.display = 'flex';
}
function closeModal() { document.getElementById('detalleModal').style.display='none'; }
document.addEventListener('DOMContentLoaded', loadHistorial);
