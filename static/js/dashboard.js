async function loadDashboard() {
  try {
    const [kpis, emociones, riesgo] = await Promise.all([
      fetch('/api/v1/kpis/general').then(r => r.json()),
      fetch('/api/v1/kpis/emociones').then(r => r.json()),
      fetch('/api/v1/kpis/riesgo').then(r => r.json()),
    ]);

    // KPI values
    const fmt = v => (v * 100).toFixed(1) + '%';
    document.getElementById('kpi-comprension') && (document.getElementById('kpi-comprension').textContent = fmt(kpis.comprension));
    document.getElementById('kpi-atencion') && (document.getElementById('kpi-atencion').textContent = fmt(kpis.atencion));
    document.getElementById('kpi-nivelacion') && (document.getElementById('kpi-nivelacion').textContent = fmt(kpis.nivelacion));
    document.getElementById('kpi-satisfaccion') && (document.getElementById('kpi-satisfaccion').textContent = fmt(kpis.satisfaccion));

    // Emotion chart
    const emotionCtx = document.getElementById('emotionChart');
    if (emotionCtx) {
      new Chart(emotionCtx, {
        type: 'doughnut',
        data: {
          labels: ['😊 Feliz', '😐 Neutral', '😢 Triste', '😠 Enojado', '😲 Sorprendido'],
          datasets: [{
            data: [emociones.feliz, emociones.neutral, emociones.triste, emociones.enojado, emociones.sorprendido],
            backgroundColor: ['#10B981', '#6B7280', '#3B82F6', '#EF4444', '#F59E0B'],
            borderWidth: 0,
          }]
        },
        options: { cutout: '65%', plugins: { legend: { position: 'bottom', labels: { padding: 12, font: { size: 12 } } } } }
      });
    }

    // Risk chart
    const riskCtx = document.getElementById('riskChart');
    if (riskCtx) {
      new Chart(riskCtx, {
        type: 'bar',
        data: {
          labels: ['🟢 Bajo', '🟡 Medio', '🔴 Alto'],
          datasets: [{
            label: 'Estudiantes',
            data: [riesgo.bajo, riesgo.medio, riesgo.alto],
            backgroundColor: ['#10B981', '#F59E0B', '#EF4444'],
            borderRadius: 8,
            borderSkipped: false,
          }]
        },
        options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, grid: { color: '#F3F4F6' } }, x: { grid: { display: false } } } }
      });
    }
  } catch (err) {
    console.error('Error loading dashboard:', err);
  }
}

function createSurvey() {
  const titulo = prompt('Título de la encuesta (ej: "Clase 5 - Algoritmos"):');
  if (!titulo) return;
  fetch('/api/v1/survey/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ titulo, teacher_id: 1, course_id: 1 })
  }).then(r => r.json()).then(data => {
    alert(`Encuesta creada.\nCódigo QR: ${data.codigo_qr}\nURL: /survey/${data.codigo_qr}`);
  });
}

document.addEventListener('DOMContentLoaded', loadDashboard);
