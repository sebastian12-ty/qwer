// ── State ──
let currentStep = 1;
const totalSteps = 5;
let cameraEnabled = false;
let videoStream = null;
let captureTimer = null;
let emotionCaptures = [];
let nlpTimer = null;

// ── Step navigation ──
function updateUI() {
  document.querySelectorAll('.survey-step').forEach((el, i) => {
    el.classList.toggle('active', i + 1 === currentStep);
  });
  const dots = document.querySelectorAll('.step-dot');
  dots.forEach((d, i) => {
    d.classList.toggle('active', i + 1 === currentStep);
    d.classList.toggle('done', i + 1 < currentStep);
  });
  document.getElementById('progressFill').style.width = ((currentStep / totalSteps) * 100) + '%';
  document.getElementById('stepLabel').textContent = `Paso ${currentStep} de ${totalSteps}`;
  document.getElementById('prevBtn').style.display = currentStep > 1 ? 'flex' : 'none';
  const next = document.getElementById('nextBtn');
  if (currentStep === 5) next.style.display = 'none';
  else next.style.display = 'flex';
  if (currentStep === 5) buildResumen();
}

function nextStep() {
  if (!validateStep()) return;
  if (currentStep < totalSteps) { currentStep++; updateUI(); window.scrollTo(0,0); }
}

function prevStep() {
  if (currentStep > 1) { currentStep--; updateUI(); window.scrollTo(0,0); }
}

function validateStep() {
  if (currentStep === 2 && !document.getElementById('calidad_clase').value) {
    alert('Por favor selecciona una calificación para la clase.'); return false;
  }
  if (currentStep === 3) {
    if (!document.getElementById('comprension_tema').value) { alert('Por favor evalúa tu comprensión.'); return false; }
    if (!document.getElementById('evaluacion_docente').value) { alert('Por favor evalúa al docente.'); return false; }
  }
  return true;
}

// ── Emoji ratings ──
document.querySelectorAll('.emoji-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    const field = this.dataset.field;
    document.querySelectorAll(`[data-field="${field}"]`).forEach(b => b.classList.remove('selected'));
    this.classList.add('selected');
    document.getElementById(field).value = this.dataset.value;
  });
});

// ── Camera ──
function toggleConsent() {
  cameraEnabled = !cameraEnabled;
  document.getElementById('toggleSwitch').classList.toggle('on', cameraEnabled);
  if (cameraEnabled) startCamera(); else stopCamera();
}

async function startCamera() {
  try {
    videoStream = await navigator.mediaDevices.getUserMedia({ video: { width: 280, height: 210 } });
    const video = document.getElementById('videoFeed');
    video.srcObject = videoStream;
    document.getElementById('cameraPreview').style.display = 'block';
    document.getElementById('cameraSection').classList.add('live');
    captureTimer = setInterval(captureFrame, 8000);
    setTimeout(captureFrame, 2000);
  } catch(e) {
    alert('No se pudo acceder a la cámara: ' + e.message);
    cameraEnabled = false;
    document.getElementById('toggleSwitch').classList.remove('on');
  }
}

function stopCamera() {
  if (videoStream) videoStream.getTracks().forEach(t => t.stop());
  if (captureTimer) clearInterval(captureTimer);
  document.getElementById('cameraSection').classList.remove('live');
  document.getElementById('cameraPreview').style.display = 'none';
}

async function captureFrame() {
  if (!videoStream) return;
  const canvas = document.createElement('canvas');
  const video = document.getElementById('videoFeed');
  canvas.width = 224; canvas.height = 168;
  canvas.getContext('2d').drawImage(video, 0, 0, 224, 168);
  const b64 = canvas.toDataURL('image/jpeg', 0.6);
  try {
    const res = await fetch('/survey/capture_emotion', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: b64 })
    });
    const data = await res.json();
    emotionCaptures.push(data);
    updateEmotionUI(data);
  } catch(e) {}
}

const emojiMap = { feliz:'😊 Feliz', neutral:'😐 Neutral', triste:'😢 Triste', enojado:'😠 Enojado', sorprendido:'😲 Sorprendido' };

function updateEmotionUI(data) {
  document.getElementById('emoLabel').textContent = emojiMap[data.predominante] || '🤔 Analizando';
  const keys = ['feliz','neutral','triste','enojado','sorprendido'];
  const max = Math.max(...keys.map(k => data[k] || 0)) || 1;
  keys.forEach(k => {
    const bar = document.getElementById('bar-' + k);
    if (bar) bar.style.height = Math.max(4, ((data[k] || 0) / max) * 28) + 'px';
  });
}

// ── NLP en tiempo real ──
document.getElementById('comentario').addEventListener('input', function() {
  clearTimeout(nlpTimer);
  const text = this.value.trim();
  if (text.length < 8) { document.getElementById('nlp-live-result').innerHTML = ''; document.getElementById('keywords-result').innerHTML = ''; return; }
  nlpTimer = setTimeout(() => analyzeNLP(text), 600);
});

async function analyzeNLP(text) {
  try {
    const res = await fetch('/api/v1/nlp/analyze', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    const colors = { positivo: '#065F46', negativo: '#991B1B', neutral: '#475569' };
    const bgs   = { positivo: '#D1FAE5', negativo: '#FEE2E2', neutral: '#F1F5F9' };
    const icons = { positivo: '😊', negativo: '😟', neutral: '😐' };
    document.getElementById('nlp-live-result').innerHTML =
      `<span class="nlp-pill ${data.label}" style="background:${bgs[data.label]};color:${colors[data.label]}">
        ${icons[data.label]} ${data.label.charAt(0).toUpperCase()+data.label.slice(1)} (${(data.score*100).toFixed(0)}%)
      </span>`;
    const kw = document.getElementById('keywords-result');
    kw.innerHTML = (data.keywords || []).map(k => `<span class="chip">${k}</span>`).join('');
  } catch(e) {}
}

// ── Resumen ──
function buildResumen() {
  const labels = { calidad_clase: 'Calidad de clase', comprension_tema: 'Comprensión', evaluacion_docente: 'Evaluación docente' };
  const emojis = { '1':'😞','2':'😕','3':'😐','4':'🙂','5':'😄' };
  let html = '';
  for (const [field, label] of Object.entries(labels)) {
    const val = document.getElementById(field)?.value;
    html += `<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #F1F5F9">
      <span style="color:#64748B">${label}</span>
      <span style="font-weight:600">${emojis[val]||'—'} ${val ? val+'/5' : 'Sin respuesta'}</span>
    </div>`;
  }
  const com = document.getElementById('comentario').value;
  if (com) html += `<div style="padding:8px 0;color:#64748B;font-size:12px">💬 "${com.substring(0,80)}${com.length>80?'...':''}"</div>`;
  if (emotionCaptures.length > 0) html += `<div style="padding:6px 0;font-size:12px;color:#64748B">📷 ${emotionCaptures.length} capturas emocionales realizadas</div>`;
  document.getElementById('resumenRespuestas').innerHTML = html;
}

// ── Submit ──
async function submitSurvey() {
  const btn = document.getElementById('submitBtn');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Analizando con IA...';
  const payload = {
    survey_id: document.getElementById('survey_id').value,
    student_id: document.getElementById('student_id').value,
    calidad_clase: document.getElementById('calidad_clase').value,
    comprension_tema: document.getElementById('comprension_tema').value,
    evaluacion_docente: document.getElementById('evaluacion_docente').value,
    comentario: document.getElementById('comentario').value,
    emotion_captures: emotionCaptures,
  };
  if (!payload.calidad_clase || !payload.comprension_tema || !payload.evaluacion_docente) {
    alert('Responde todas las preguntas antes de enviar.'); btn.disabled=false; btn.innerHTML='<i class="fas fa-paper-plane"></i> Enviar'; return;
  }
  try {
    const res = await fetch('/survey/submit', {
      method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.status === 'ok') {
      stopCamera();
      document.getElementById('confirmCard').style.display = 'none';
      document.getElementById('resultadoFinal').style.display = 'block';
      document.getElementById('prevBtn').style.display = 'none';
      renderResultado(data.kpis);
    }
  } catch(e) {
    alert('Error al enviar. Intenta de nuevo.');
    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-paper-plane"></i> Enviar Encuesta';
  }
}

function renderResultado(kpis) {
  const items = [
    { label:'Comprensión', val: kpis.indice_comprension, color:'#4F46E5' },
    { label:'Atención',    val: kpis.indice_atencion,    color:'#06B6D4' },
    { label:'Nivelación',  val: kpis.indice_nivelacion,  color:'#10B981' },
    { label:'Coherencia',  val: kpis.indice_coherencia_emocional, color:'#F59E0B' },
  ];
  document.getElementById('resultKpis').innerHTML = items.map(i => `
    <div class="result-kpi-item">
      <div class="result-kpi-val" style="color:${i.color}">${((i.val||0)*100).toFixed(1)}%</div>
      <div class="result-kpi-label">${i.label}</div>
    </div>`).join('');
  const riesgo = kpis.riesgo_insatisfaccion;
  const rmap = { bajo: ['#D1FAE5','#065F46','🟢'], medio: ['#FEF3C7','#92400E','🟡'], alto: ['#FEE2E2','#991B1B','🔴'] };
  const [bg,color,icon] = rmap[riesgo] || rmap.medio;
  document.getElementById('resultRiesgo').innerHTML =
    `<div style="background:${bg};color:${color};padding:12px;border-radius:10px">${icon} Nivel de riesgo académico: <b>${riesgo.toUpperCase()}</b></div>`;
}

// ── Init ──
updateUI();
