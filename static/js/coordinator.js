async function loadCoordinator() {
  const [kpis, riesgo] = await Promise.all([
    fetch('/api/v1/kpis/general').then(r=>r.json()).catch(()=>({})),
    fetch('/api/v1/kpis/riesgo').then(r=>r.json()).catch(()=>({})),
  ]);
  const fmt = v => v != null ? (v*100).toFixed(1)+'%' : '—';
  const set = (id, v) => { const el=document.getElementById(id); if(el) el.textContent=v; };
  set('k-total',       kpis.total_respuestas ?? '—');
  set('k-niv',         fmt(kpis.nivelacion));
  set('k-comp',        fmt(kpis.comprension));
  set('k-riesgo-alto', riesgo.alto ?? '—');
}
document.addEventListener('DOMContentLoaded', loadCoordinator);
