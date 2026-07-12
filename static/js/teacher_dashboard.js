async function loadTeacher() {
  const [enc] = await Promise.all([
    fetch('/api/v1/teacher/encuestas').then(r=>r.json()).catch(()=>({surveys:[]})),
  ]);
  const surveys = enc.surveys || [];

  // Encuestas rápidas (topbar widget)
  const wrap = document.getElementById('encuestas-rapidas');
  if (wrap) {
    wrap.innerHTML = surveys.length
      ? surveys.slice(0,4).map(s => `
          <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:10px 14px;font-size:12px">
            <div style="font-weight:700;color:#0F172A;margin-bottom:2px">${s.titulo}</div>
            <div style="color:#64748B;display:flex;align-items:center;gap:8px">
              <span>${s.respuestas} resp.</span>
              <code style="background:#EEF2FF;color:#4F46E5;padding:1px 6px;border-radius:4px">${s.codigo_qr}</code>
              <a href="/survey/${s.codigo_qr}" target="_blank" style="color:#4F46E5"><i class="fas fa-external-link-alt"></i></a>
            </div>
          </div>`).join('')
      : '<span style="font-size:13px;color:#94A3B8">Sin encuestas. <a href="/teacher/nueva-encuesta">Crear una</a></span>';
  }

  // Tabla de encuestas (dashboard)
  const tbody = document.getElementById('encuestasBody');
  if (tbody) {
    tbody.innerHTML = surveys.length
      ? surveys.map(s => `<tr>
          <td style="font-weight:600">${s.titulo}</td>
          <td><code style="background:#EEF2FF;color:#4F46E5;padding:2px 8px;border-radius:5px;font-size:11px">${s.codigo_qr}</code></td>
          <td>${s.respuestas}</td>
          <td style="color:#4F46E5;font-weight:700">${s.nivelacion_prom ? (s.nivelacion_prom*100).toFixed(1)+'%' : '—'}</td>
          <td><span class="badge ${s.activa?'badge-success':'badge-neutral'}">${s.activa?'Activa':'Cerrada'}</span></td>
          <td><a href="/survey/${s.codigo_qr}" target="_blank" class="btn btn-ghost btn-sm"><i class="fas fa-external-link-alt"></i></a></td>
        </tr>`).join('')
      : '<tr><td colspan="6" style="text-align:center;padding:24px;color:#94A3B8">Sin encuestas. <a href="/teacher/nueva-encuesta">Crear una</a></td></tr>';
    document.getElementById('encuestas-count') && (document.getElementById('encuestas-count').textContent = surveys.length + ' encuestas');
  }
}

// Nueva encuesta form
const form = document.getElementById('nuevaEncuestaForm');
if (form) {
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const btn = form.querySelector('button[type=submit]');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Creando...';
    const data = await fetch('/api/v1/survey/create', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        titulo:     document.getElementById('titulo').value,
        teacher_id: 1,
        course_id:  parseInt(document.getElementById('course_id').value) || 1,
      }),
    }).then(r=>r.json()).catch(()=>({}));
    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-qrcode"></i> Generar Encuesta y QR';
    if (data.codigo_qr) {
      document.getElementById('qrCode').textContent = data.codigo_qr;
      document.getElementById('qrLink').href = '/survey/' + data.codigo_qr;
      document.getElementById('qrResult').style.display = 'block';
      document.getElementById('qrResult').scrollIntoView({ behavior: 'smooth' });
    }
  });
}

function crearEncuesta() { window.location.href = '/teacher/nueva-encuesta'; }

document.addEventListener('DOMContentLoaded', loadTeacher);
