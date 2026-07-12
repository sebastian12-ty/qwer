const CHART_COLORS = { comprension:'#4F46E5', atencion:'#06B6D4', nivelacion:'#10B981', coherencia:'#F59E0B' };

async function loadStudentDashboard() {
  const [kpis, emociones, historial] = await Promise.all([
    fetch('/api/v1/kpis/general').then(r=>r.json()).catch(()=>({})),
    fetch('/api/v1/kpis/emociones').then(r=>r.json()).catch(()=>({})),
    fetch('/api/v1/student/historial?limit=10').then(r=>r.json()).catch(()=>({rows:[]})),
  ]);
  const fmt = v => v != null ? (v*100).toFixed(1)+'%' : '—';
  document.getElementById('kpi-comprension').textContent = fmt(kpis.comprension);
  document.getElementById('kpi-atencion').textContent    = fmt(kpis.atencion);
  document.getElementById('kpi-nivelacion').textContent  = fmt(kpis.nivelacion);
  document.getElementById('kpi-coherencia').textContent  = fmt(kpis.coherencia);
  document.getElementById('dash-total-encuestas').textContent = kpis.total_respuestas || 0;
  document.getElementById('dash-prom-nivelacion').textContent = fmt(kpis.nivelacion);

  const emoMax = Object.entries(emociones).sort((a,b)=>b[1]-a[1])[0];
  const emojiM = { feliz:'😊', neutral:'😐', triste:'😢', enojado:'😠', sorprendido:'😲' };
  document.getElementById('dash-emocion-top').textContent = emojiM[emoMax?.[0]] || '—';

  // Evolución chart
  const rows = historial.rows || [];
  new Chart(document.getElementById('evolucionChart'), {
    type: 'line',
    data: {
      labels: rows.map((_,i) => `E${i+1}`),
      datasets: [
        { label:'Comprensión', data: rows.map(r=>(r.indice_comprension||0)*100), borderColor:'#4F46E5', tension:.4, fill:false, pointRadius:4 },
        { label:'Nivelación',  data: rows.map(r=>(r.indice_nivelacion||0)*100),  borderColor:'#10B981', tension:.4, fill:false, pointRadius:4 },
        { label:'Atención',    data: rows.map(r=>(r.indice_atencion||0)*100),    borderColor:'#06B6D4', tension:.4, fill:false, pointRadius:4 },
      ]
    },
    options: { plugins:{legend:{position:'bottom',labels:{boxWidth:10,font:{size:11}}}}, scales:{ y:{min:0,max:100,grid:{color:'#F1F5F9'}}, x:{grid:{display:false}} }, responsive:true }
  });

  // Emoción chart
  new Chart(document.getElementById('emocionChart'), {
    type: 'doughnut',
    data: {
      labels: ['😊 Feliz','😐 Neutral','😢 Triste','😠 Enojado','😲 Sorprendido'],
      datasets: [{ data: [emociones.feliz,emociones.neutral,emociones.triste,emociones.enojado,emociones.sorprendido].map(v=>(v||0)*100),
        backgroundColor:['#10B981','#94A3B8','#3B82F6','#EF4444','#F59E0B'], borderWidth:0 }]
    },
    options: { cutout:'65%', plugins:{ legend:{ position:'bottom', labels:{ boxWidth:10, font:{size:11} } } } }
  });

  // Tabla últimas encuestas
  const tbody = document.getElementById('ultimas-encuestas-body');
  if (!rows.length) { tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:24px;color:#94A3B8">Sin encuestas respondidas aún</td></tr>'; return; }
  const rmap = { bajo:'badge-success', medio:'badge-warning', alto:'badge-danger' };
  const emojiM2 = { feliz:'😊', neutral:'😐', triste:'😢', enojado:'😠', sorprendido:'😲' };
  tbody.innerHTML = rows.map(r => `<tr>
    <td>${new Date(r.fecha).toLocaleDateString('es-PE')}</td>
    <td>${r.curso||'—'}</td>
    <td style="font-weight:700;color:#4F46E5">${((r.indice_nivelacion||0)*100).toFixed(1)}%</td>
    <td>${emojiM2[r.emocion_predominante]||'—'} ${r.emocion_predominante||'—'}</td>
    <td><span class="badge ${rmap[r.riesgo_insatisfaccion]||'badge-neutral'}">${r.riesgo_insatisfaccion||'—'}</span></td>
  </tr>`).join('');
}

document.addEventListener('DOMContentLoaded', loadStudentDashboard);
