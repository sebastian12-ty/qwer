async function loadPerfil() {
  const [kpis, emociones] = await Promise.all([
    fetch('/api/v1/kpis/general').then(r=>r.json()).catch(()=>({})),
    fetch('/api/v1/kpis/emociones').then(r=>r.json()).catch(()=>({})),
  ]);
  const emojiM = { feliz:'😊', neutral:'😐', triste:'😢', enojado:'😠', sorprendido:'😲' };
  const emoMax = Object.entries(emociones).sort((a,b)=>b[1]-a[1])[0];
  document.getElementById('emocion-predominante-perfil').textContent = emojiM[emoMax?.[0]] || '—';
  document.getElementById('emocion-label-perfil').textContent = (emoMax?.[0]||'—').charAt(0).toUpperCase()+(emoMax?.[0]||'').slice(1);
  const riesgo = kpis.nivelacion >= 0.7 ? 'bajo' : kpis.nivelacion >= 0.5 ? 'medio' : 'alto';
  const rmap = { bajo:['#D1FAE5','#065F46','🟢 Riesgo bajo'], medio:['#FEF3C7','#92400E','🟡 Riesgo medio'], alto:['#FEE2E2','#991B1B','🔴 Riesgo alto'] };
  const [bg,color,label] = rmap[riesgo];
  document.getElementById('riesgo-perfil').innerHTML = `<span style="background:${bg};color:${color};padding:6px 14px;border-radius:20px;font-size:12px;font-weight:700">${label}</span>`;

  // Radar
  new Chart(document.getElementById('radarChart'), {
    type: 'radar',
    data: {
      labels: ['Comprensión','Atención','Nivelación','Coherencia','Satisfacción'],
      datasets: [{ label:'Mi perfil',
        data: [kpis.comprension,kpis.atencion,kpis.nivelacion,kpis.coherencia,kpis.satisfaccion].map(v=>(v||0)*100),
        backgroundColor:'rgba(79,70,229,.15)', borderColor:'#4F46E5', pointBackgroundColor:'#4F46E5', pointRadius:4 }]
    },
    options: { scales:{ r:{ min:0, max:100, ticks:{stepSize:25,font:{size:10}}, grid:{color:'#E2E8F0'}, pointLabels:{font:{size:11}} } }, plugins:{legend:{display:false}} }
  });

  // Tendencia (fake de ejemplo si no hay datos)
  const hist = await fetch('/api/v1/student/historial?limit=8').then(r=>r.json()).catch(()=>({rows:[]}));
  const rows = hist.rows || [];
  new Chart(document.getElementById('tendenciaChart'), {
    type: 'line',
    data: {
      labels: rows.length ? rows.map((_,i)=>`E${i+1}`) : ['E1','E2','E3','E4','E5'],
      datasets: [
        { label:'Nivelación', data: rows.length ? rows.map(r=>(r.indice_nivelacion||0)*100) : [55,60,65,70,72], borderColor:'#4F46E5', tension:.4, fill:true, backgroundColor:'rgba(79,70,229,.05)' },
        { label:'Comprensión', data: rows.length ? rows.map(r=>(r.indice_comprension||0)*100) : [50,58,62,68,75], borderColor:'#10B981', tension:.4, fill:false },
      ]
    },
    options: { plugins:{legend:{position:'bottom',labels:{boxWidth:10,font:{size:11}}}}, scales:{ y:{min:0,max:100,grid:{color:'#F1F5F9'}}, x:{grid:{display:false}} } }
  });

  // IA Analysis
  const niv = (kpis.nivelacion||0)*100;
  const comp = (kpis.comprension||0)*100;
  const aten = (kpis.atencion||0)*100;
  let analisis = '';
  if (niv >= 70) analisis += '✅ Tu índice de nivelación es <b>sólido</b>. Estás asimilando bien los contenidos de clase. ';
  else if (niv >= 50) analisis += '⚠️ Tu nivelación es <b>moderada</b>. Podrías reforzar con material adicional o consultar al docente. ';
  else analisis += '🔴 Tu nivelación es <b>baja</b>. Se recomienda tutorías adicionales y revisión de los temas. ';
  if (comp >= 70) analisis += '<br>💡 Demuestras una buena <b>comprensión</b> de los temas explicados en clase. ';
  else analisis += '<br>📚 Tu comprensión puede mejorar. Intenta repasar el material después de cada clase. ';
  if (aten >= 60) analisis += '<br>👁️ Tus expresiones faciales indican un nivel <b>adecuado de atención</b> durante las sesiones. ';
  else analisis += '<br>👁️ El análisis facial sugiere cierta <b>distracción</b>. Intenta sentarte cerca y minimizar distracciones. ';
  document.getElementById('ia-analisis').innerHTML = analisis;
}
document.addEventListener('DOMContentLoaded', loadPerfil);
