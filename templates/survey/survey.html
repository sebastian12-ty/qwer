<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Encuesta — {{ survey.titulo }}</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<link rel="stylesheet" href="/static/css/main.css">
<style>
  body { background: linear-gradient(135deg,#EEF2FF 0%,#E0F7FA 100%); min-height:100vh; }
  .survey-wrap { max-width:700px; margin:0 auto; padding:24px 16px 100px; }

  /* Progress bar top */
  .prog-top { position:fixed;top:0;left:0;right:0;height:4px;background:#E2E8F0;z-index:200; }
  .prog-fill { height:4px;background:linear-gradient(90deg,#4F46E5,#06B6D4);transition:width .5s ease; }

  /* Header */
  .survey-header { text-align:center;padding:20px 0 28px; }
  .survey-header h2 { font-size:18px;font-weight:800;color:#0F172A;margin-bottom:4px; }
  .survey-header p  { font-size:13px;color:#64748B; }

  /* Step dots */
  .step-dots { display:flex;gap:8px;justify-content:center;margin-top:14px; }
  .dot { width:8px;height:8px;border-radius:50%;background:#E2E8F0;transition:all .3s; }
  .dot.active { background:#4F46E5;transform:scale(1.4); }
  .dot.done   { background:#10B981; }

  /* Steps */
  .step { display:none; animation:fadeUp .3s ease; }
  .step.active { display:block; }
  @keyframes fadeUp { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:none} }

  /* Card */
  .s-card { background:#fff;border-radius:16px;padding:26px;box-shadow:0 2px 12px rgba(0,0,0,.07);margin-bottom:14px; }
  .q-num  { display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;background:#EEF2FF;color:#4F46E5;border-radius:8px;font-size:13px;font-weight:700;margin-bottom:10px; }
  .q-title{ font-size:16px;font-weight:700;margin-bottom:4px; }
  .q-sub  { font-size:13px;color:#64748B;margin-bottom:18px; }

  /* Emoji rating */
  .emoji-row { display:flex;gap:8px;justify-content:center; }
  .e-btn { flex:1;max-width:120px;padding:14px 6px;border:2px solid #E2E8F0;border-radius:14px;cursor:pointer;text-align:center;transition:all .18s;background:#fff; }
  .e-btn:hover  { border-color:#4F46E5;background:#EEF2FF;transform:scale(1.05); }
  .e-btn.sel    { border-color:#4F46E5;background:#4F46E5;color:#fff; }
  .e-btn .emj   { font-size:26px;display:block;margin-bottom:5px; }
  .e-btn .lbl   { font-size:10px;font-weight:600;color:#64748B; }
  .e-btn.sel .lbl { color:rgba(255,255,255,.85); }

  /* Camera */
  .cam-wrap { border:2px dashed #CBD5E1;border-radius:14px;padding:20px;text-align:center;transition:.2s; }
  .cam-wrap.live { border-color:#10B981;border-style:solid;background:#F0FDF4; }
  .consent-row { display:flex;align-items:center;gap:12px;padding:12px 16px;background:#F8FAFC;border-radius:10px;cursor:pointer;user-select:none; }
  .toggle { width:42px;height:24px;background:#CBD5E1;border-radius:12px;position:relative;transition:.3s;flex-shrink:0; }
  .toggle.on { background:#4F46E5; }
  .toggle::after { content:'';position:absolute;width:20px;height:20px;background:#fff;border-radius:50%;top:2px;left:2px;transition:.3s;box-shadow:0 1px 4px rgba(0,0,0,.2); }
  .toggle.on::after { left:20px; }

  /* Video + canvas overlay */
  .video-box { position:relative;display:inline-block;border-radius:12px;overflow:hidden;margin-top:14px; }
  #videoEl { display:block;width:300px;height:225px;object-fit:cover; }
  #overlayCanvas { position:absolute;top:0;left:0;width:300px;height:225px;pointer-events:none; }

  /* Emotion HUD */
  .emo-hud { background:rgba(0,0,0,.72);backdrop-filter:blur(6px);border-radius:0 0 12px 12px;padding:8px 12px; }
  .emo-row  { display:flex;align-items:center;gap:8px;justify-content:space-between; }
  .emo-main { font-size:13px;font-weight:700;color:#fff; }
  .emo-bars { display:flex;gap:4px;align-items:flex-end;height:28px; }
  .emo-bar  { width:8px;border-radius:3px 3px 0 0;transition:height .4s;min-height:3px; }
  .tracking-pills { display:flex;gap:6px;margin-top:6px;flex-wrap:wrap; }
  .tpill { font-size:10px;font-weight:600;padding:2px 8px;border-radius:20px; }
  .tpill.on  { background:#10B981;color:#fff; }
  .tpill.off { background:rgba(255,255,255,.15);color:rgba(255,255,255,.6); }

  /* NLP live */
  .nlp-live { margin-top:10px;min-height:30px; }
  .nlp-pill { display:inline-flex;align-items:center;gap:6px;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600; }
  .nlp-pill.positivo { background:#D1FAE5;color:#065F46; }
  .nlp-pill.negativo { background:#FEE2E2;color:#991B1B; }
  .nlp-pill.neutral  { background:#F1F5F9;color:#475569; }
  .kw-wrap { display:flex;flex-wrap:wrap;gap:4px;margin-top:6px; }
  .chip { font-size:11px;padding:2px 8px;background:#F1F5F9;border:1px solid #E2E8F0;border-radius:20px;color:#475569; }

  /* Nav bar */
  .nav-bar { position:fixed;bottom:0;left:0;right:0;background:rgba(255,255,255,.94);backdrop-filter:blur(10px);border-top:1px solid #E2E8F0;padding:12px 24px;display:flex;align-items:center;justify-content:space-between;z-index:100; }
  .step-lbl { font-size:12px;color:#64748B; }

  /* Result KPIs */
  .result-grid { display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px; }
  .result-kpi  { background:#F8FAFC;border-radius:12px;padding:16px;text-align:center; }
  .result-val  { font-size:26px;font-weight:800; }
  .result-lbl  { font-size:11px;color:#64748B;margin-top:3px; }
</style>
</head>
<body>

<div class="prog-top"><div class="prog-fill" id="progFill" style="width:20%"></div></div>

<div class="survey-wrap">
  <div class="survey-header">
    <div style="font-size:32px;margin-bottom:6px">📋</div>
    <h2>{{ survey.titulo }}</h2>
    <p>Tu opinión mejora la calidad educativa</p>
    <div class="step-dots" id="stepDots">
      <div class="dot active"></div>
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
    </div>
  </div>

  <!-- PASO 1: Cámara + consentimiento -->
  <div class="step active" id="step-1">
    <div class="s-card">
      <div class="q-num">📷</div>
      <div class="q-title">Análisis emocional con IA</div>
      <div class="q-sub">La cámara captura tu expresión facial para medir tu nivel de atención y bienestar. Opcional y ético — las imágenes no se guardan.</div>

      <div class="cam-wrap" id="camWrap">
        <div class="consent-row" onclick="toggleCam()">
          <div class="toggle" id="toggle"></div>
          <div style="text-align:left">
            <div style="font-size:13px;font-weight:600">Activar análisis facial con IA</div>
            <div style="font-size:11px;color:#64748B">Detecta cara, ojos, sonrisa y emociones en tiempo real</div>
          </div>
        </div>

        <div id="camPreview" style="display:none">
          <div class="video-box" style="margin:0 auto;display:block;width:300px">
            <video id="videoEl" autoplay muted playsinline></video>
            <canvas id="overlayCanvas"></canvas>
          </div>
          <div class="emo-hud">
            <div class="emo-row">
              <span class="emo-main" id="emoMain">🔍 Iniciando...</span>
              <div class="emo-bars">
                <div class="emo-bar" id="b-feliz"      style="background:#34D399;height:4px" title="Feliz"></div>
                <div class="emo-bar" id="b-neutral"    style="background:#94A3B8;height:4px" title="Neutral"></div>
                <div class="emo-bar" id="b-triste"     style="background:#60A5FA;height:4px" title="Triste"></div>
                <div class="emo-bar" id="b-enojado"    style="background:#F87171;height:4px" title="Enojado"></div>
                <div class="emo-bar" id="b-sorprendido" style="background:#FBBF24;height:4px" title="Sorprendido"></div>
              </div>
            </div>
            <div class="tracking-pills" id="trackPills">
              <span class="tpill off" id="pill-face">😶 Cara</span>
              <span class="tpill off" id="pill-eyes">👁 Ojos</span>
              <span class="tpill off" id="pill-smile">😊 Sonrisa</span>
              <span class="tpill off" id="pill-attention">🎯 Atención</span>
            </div>
          </div>
        </div>

        <div id="camOff" style="padding:20px 0;color:#94A3B8;font-size:13px">
          <i class="fas fa-camera" style="font-size:24px;display:block;margin-bottom:8px"></i>
          Haz clic arriba para activar la cámara
        </div>
      </div>
    </div>
  </div>

  <!-- PASO 2: Calidad clase -->
  <div class="step" id="step-2">
    <div class="s-card">
      <div class="q-num">1</div>
      <div class="q-title">¿Cómo califica la clase de hoy?</div>
      <div class="q-sub">Evalúa el contenido, dinámica y organización general</div>
      <div class="emoji-row">
        <div class="e-btn" data-field="calidad_clase" data-value="1"><span class="emj">😞</span><span class="lbl">Muy mala</span></div>
        <div class="e-btn" data-field="calidad_clase" data-value="2"><span class="emj">😕</span><span class="lbl">Mala</span></div>
        <div class="e-btn" data-field="calidad_clase" data-value="3"><span class="emj">😐</span><span class="lbl">Regular</span></div>
        <div class="e-btn" data-field="calidad_clase" data-value="4"><span class="emj">🙂</span><span class="lbl">Buena</span></div>
        <div class="e-btn" data-field="calidad_clase" data-value="5"><span class="emj">😄</span><span class="lbl">Excelente</span></div>
      </div>
      <input type="hidden" id="calidad_clase">
    </div>
  </div>

  <!-- PASO 3: Comprensión + docente -->
  <div class="step" id="step-3">
    <div class="s-card">
      <div class="q-num">2</div>
      <div class="q-title">¿Qué tan bien comprendiste los temas?</div>
      <div class="q-sub">Evalúa tu nivel de comprensión al finalizar la sesión</div>
      <div class="emoji-row">
        <div class="e-btn" data-field="comprension_tema" data-value="1"><span class="emj">🤯</span><span class="lbl">Nada</span></div>
        <div class="e-btn" data-field="comprension_tema" data-value="2"><span class="emj">😵</span><span class="lbl">Poco</span></div>
        <div class="e-btn" data-field="comprension_tema" data-value="3"><span class="emj">🤔</span><span class="lbl">Más o menos</span></div>
        <div class="e-btn" data-field="comprension_tema" data-value="4"><span class="emj">🧠</span><span class="lbl">Bastante</span></div>
        <div class="e-btn" data-field="comprension_tema" data-value="5"><span class="emj">💡</span><span class="lbl">Totalmente</span></div>
      </div>
      <input type="hidden" id="comprension_tema">
    </div>
    <div class="s-card">
      <div class="q-num">3</div>
      <div class="q-title">¿Cómo evalúas al docente?</div>
      <div class="q-sub">Didáctica, claridad y dominio del tema</div>
      <div class="emoji-row">
        <div class="e-btn" data-field="evaluacion_docente" data-value="1"><span class="emj">👎</span><span class="lbl">Muy malo</span></div>
        <div class="e-btn" data-field="evaluacion_docente" data-value="2"><span class="emj">😤</span><span class="lbl">Malo</span></div>
        <div class="e-btn" data-field="evaluacion_docente" data-value="3"><span class="emj">😶</span><span class="lbl">Regular</span></div>
        <div class="e-btn" data-field="evaluacion_docente" data-value="4"><span class="emj">👍</span><span class="lbl">Bueno</span></div>
        <div class="e-btn" data-field="evaluacion_docente" data-value="5"><span class="emj">🏆</span><span class="lbl">Excelente</span></div>
      </div>
      <input type="hidden" id="evaluacion_docente">
    </div>
  </div>

  <!-- PASO 4: Comentario + NLP live -->
  <div class="step" id="step-4">
    <div class="s-card">
      <div class="q-num">4</div>
      <div class="q-title">Comentarios y sugerencias</div>
      <div class="q-sub">La IA analiza tu texto en tiempo real para detectar sentimiento y palabras clave</div>
      <textarea id="comentario" class="form-control" rows="5" placeholder="Ej: La clase estuvo muy clara, aunque hubiera preferido más ejemplos prácticos..."></textarea>
      <div class="nlp-live" id="nlpLive"></div>
      <div class="kw-wrap"  id="kwWrap"></div>
    </div>
  </div>

  <!-- PASO 5: Confirmar + resultado -->
  <div class="step" id="step-5">
    <div class="s-card" id="confirmCard">
      <div style="text-align:center;padding:8px 0 16px">
        <div style="font-size:40px;margin-bottom:10px">✅</div>
        <div style="font-size:17px;font-weight:800;margin-bottom:6px">Revisa tu encuesta</div>
        <div style="font-size:13px;color:#64748B">Confirma tus respuestas antes de enviar</div>
      </div>
      <div id="resumen" style="background:#F8FAFC;border-radius:10px;padding:16px;margin-bottom:16px;font-size:13px"></div>
      <button class="btn btn-primary btn-lg w-full" id="submitBtn" onclick="submitSurvey()">
        <i class="fas fa-paper-plane"></i> Enviar encuesta
      </button>
    </div>
    <div id="resultadoFinal" style="display:none">
      <div class="s-card" style="text-align:center">
        <div style="font-size:52px;margin-bottom:10px">🎉</div>
        <div style="font-size:20px;font-weight:800;margin-bottom:6px">¡Encuesta enviada!</div>
        <div style="font-size:13px;color:#64748B;margin-bottom:4px">Gracias por tu participación</div>
        <div class="result-grid" id="resultKpis"></div>
        <div id="resultRiesgo" style="margin-top:14px;padding:12px;border-radius:10px;font-size:13px;font-weight:600"></div>
        <div style="margin-top:20px;display:flex;gap:10px;justify-content:center">
          <a href="/student/dashboard" class="btn btn-primary"><i class="fas fa-home"></i> Inicio</a>
          <a href="/student/historial"  class="btn btn-outline"><i class="fas fa-history"></i> Historial</a>
        </div>
      </div>
    </div>
  </div>

</div><!-- end survey-wrap -->

<!-- Nav bottom -->
<div class="nav-bar">
  <button class="btn btn-outline" id="prevBtn" onclick="prevStep()" style="display:none"><i class="fas fa-arrow-left"></i> Atrás</button>
  <span class="step-lbl" id="stepLbl">Paso 1 de 5</span>
  <button class="btn btn-primary" id="nextBtn" onclick="nextStep()">Siguiente <i class="fas fa-arrow-right"></i></button>
</div>

<input type="hidden" id="survey_id"  value="{{ survey.id }}">
<input type="hidden" id="student_id" value="1">

<script>
// ── State ──────────────────────────────────────────────
let step = 1;
const TOTAL = 5;
let videoStream   = null;
let captureTimer  = null;
let nlpTimer      = null;
let emoCaptures   = [];
const EMOJIS = { feliz:'😊 Feliz', neutral:'😐 Neutral', triste:'😢 Triste', enojado:'😠 Enojado', sorprendido:'😲 Sorprendido' };

// ── Navigation ─────────────────────────────────────────
function updateUI() {
  document.querySelectorAll('.step').forEach((el,i) => el.classList.toggle('active', i+1===step));
  document.querySelectorAll('.dot').forEach((d,i) => {
    d.classList.toggle('active', i+1===step);
    d.classList.toggle('done',   i+1<step);
  });
  document.getElementById('progFill').style.width = (step/TOTAL*100)+'%';
  document.getElementById('stepLbl').textContent  = `Paso ${step} de ${TOTAL}`;
  document.getElementById('prevBtn').style.display = step>1 ? 'flex' : 'none';
  document.getElementById('nextBtn').style.display = step===5 ? 'none' : 'flex';
  if (step===5) buildResumen();
  window.scrollTo({top:0, behavior:'smooth'});
}

function nextStep() {
  if (!validate()) return;
  if (step < TOTAL) { step++; updateUI(); }
}
function prevStep() { if (step>1) { step--; updateUI(); } }

function validate() {
  const checks = { 2:'calidad_clase', 3:'comprension_tema' };
  if (checks[step] && !document.getElementById(checks[step]).value) {
    shakePage(); return false;
  }
  if (step===3 && !document.getElementById('evaluacion_docente').value) { shakePage(); return false; }
  return true;
}
function shakePage() {
  document.querySelector('.step.active').style.animation='none';
  setTimeout(()=>document.querySelector('.step.active').style.animation='', 50);
}

// ── Emoji rating ───────────────────────────────────────
document.querySelectorAll('.e-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    const field = this.dataset.field;
    document.querySelectorAll(`[data-field="${field}"]`).forEach(b=>b.classList.remove('sel'));
    this.classList.add('sel');
    document.getElementById(field).value = this.dataset.value;
  });
});

// ── Camera & tracking ──────────────────────────────────
function toggleCam() {
  const tog = document.getElementById('toggle');
  tog.classList.toggle('on');
  if (tog.classList.contains('on')) startCam(); else stopCam();
}

async function startCam() {
  try {
    videoStream = await navigator.mediaDevices.getUserMedia({
      video: { width:{ ideal:640 }, height:{ ideal:480 }, facingMode:'user' }
    });
    const vid = document.getElementById('videoEl');
    vid.srcObject = videoStream;
    document.getElementById('camPreview').style.display = 'block';
    document.getElementById('camOff').style.display     = 'none';
    document.getElementById('camWrap').classList.add('live');
    captureTimer = setInterval(captureAndAnalyze, 6000);
    setTimeout(captureAndAnalyze, 1500); // first capture fast
    startLocalTracking(); // canvas overlay
  } catch(e) {
    alert('No se pudo acceder a la cámara: ' + e.message);
    document.getElementById('toggle').classList.remove('on');
  }
}

function stopCam() {
  if (videoStream) videoStream.getTracks().forEach(t=>t.stop());
  if (captureTimer) clearInterval(captureTimer);
  document.getElementById('camPreview').style.display = 'none';
  document.getElementById('camOff').style.display     = 'block';
  document.getElementById('camWrap').classList.remove('live');
}

// ── Canvas overlay (client-side face box) ─────────────
let localTrackTimer = null;
function startLocalTracking() {
  const vid = document.getElementById('videoEl');
  const cvs = document.getElementById('overlayCanvas');
  const ctx = cvs.getContext('2d');
  cvs.width  = 300; cvs.height = 225;

  function drawFrame() {
    ctx.clearRect(0,0,300,225);
    // Simple brightness-based "face zone" indicator (no JS face detection available client-side without heavy libs)
    // Draw a guide rectangle where face should be
    const isLive = videoStream && videoStream.active;
    if (isLive) {
      ctx.strokeStyle = 'rgba(79,70,229,0.5)';
      ctx.lineWidth   = 1.5;
      ctx.setLineDash([5,5]);
      ctx.strokeRect(60, 20, 180, 185); // face guide zone
      ctx.setLineDash([]);
      ctx.fillStyle = 'rgba(79,70,229,0.12)';
      ctx.fillRect(60,20,180,185);
      ctx.fillStyle = 'rgba(79,70,229,0.7)';
      ctx.font = '10px Inter, sans-serif';
      ctx.fillText('Zona facial', 100, 14);
    }
  }
  localTrackTimer = setInterval(drawFrame, 200);
}

// ── Capture & analyze ──────────────────────────────────
async function captureAndAnalyze() {
  if (!videoStream || !videoStream.active) return;
  const vid = document.getElementById('videoEl');
  const cvs = document.createElement('canvas');
  cvs.width = 320; cvs.height = 240;
  cvs.getContext('2d').drawImage(vid, 0, 0, 320, 240);
  const b64 = cvs.toDataURL('image/jpeg', 0.75);

  try {
    const res  = await fetch('/survey/capture_emotion', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ image: b64 })
    });
    const data = await res.json();
    emoCaptures.push(data);
    updateEmoHUD(data);
    updateOverlay(data);
  } catch(e) { console.warn('Capture error:', e); }
}

function updateEmoHUD(data) {
  // Main label
  const main = document.getElementById('emoMain');
  main.textContent = EMOJIS[data.predominante] || '🤔 Analizando';

  // Bars
  const keys = ['feliz','neutral','triste','enojado','sorprendido'];
  const max  = Math.max(...keys.map(k=>data[k]||0)) || 1;
  keys.forEach(k => {
    const bar = document.getElementById('b-'+k);
    if (bar) bar.style.height = Math.max(4, ((data[k]||0)/max)*26)+'px';
  });

  // Tracking pills
  const tr = data.tracking || {};
  setPill('pill-face',      tr.face_detected,  '😶 Cara',     '😶 Cara');
  setPill('pill-eyes',      tr.eyes_detected,  '👁 Ojos',     '👁 Ojos');
  setPill('pill-smile',     tr.smile_detected, '😊 Sonrisa',  '😊 Sonrisa');
  setPill('pill-attention', tr.face_detected && tr.eyes_detected, '🎯 Atención', '🎯 Atención');
}

function setPill(id, active, label) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = label;
  el.classList.toggle('on',  !!active);
  el.classList.toggle('off', !active);
}

function updateOverlay(data) {
  const cvs = document.getElementById('overlayCanvas');
  const ctx = cvs.getContext('2d');
  ctx.clearRect(0,0,300,225);

  const tr = data.tracking || {};
  if (tr.face_detected && tr.face_position) {
    const fp = tr.face_position;
    // Scale from 320x240 to 300x225
    const sx = 300/320, sy = 225/240;
    const x = fp.x*sx, y = fp.y*sy, w = fp.w*sx, h = fp.h*sy;

    // Face box
    ctx.strokeStyle = '#10B981';
    ctx.lineWidth   = 2.5;
    ctx.shadowColor = 'rgba(16,185,129,.4)';
    ctx.shadowBlur  = 6;
    ctx.strokeRect(x, y, w, h);
    ctx.shadowBlur  = 0;

    // Corner decorators
    const cs = 12;
    ctx.strokeStyle = '#4F46E5';
    ctx.lineWidth   = 3;
    [[x,y],[x+w,y],[x,y+h],[x+w,y+h]].forEach(([cx,cy]) => {
      ctx.beginPath();
      ctx.moveTo(cx+(cx<x+w/2?cs:-cs), cy); ctx.lineTo(cx,cy); ctx.lineTo(cx, cy+(cy<y+h/2?cs:-cs));
      ctx.stroke();
    });

    // Emotion label above face box
    const emoText = (data.predominante||'').toUpperCase();
    ctx.fillStyle = 'rgba(79,70,229,.85)';
    ctx.fillRect(x, y-22, emoText.length*8+12, 20);
    ctx.fillStyle = '#fff';
    ctx.font      = 'bold 11px Inter, sans-serif';
    ctx.fillText(emoText, x+6, y-7);

    // Eyes dots
    if (tr.eyes_detected) {
      ctx.fillStyle = '#34D399';
      ctx.shadowColor = '#34D399'; ctx.shadowBlur = 4;
      // approximate eye positions within face box
      [[x+w*0.3, y+h*0.35],[x+w*0.7, y+h*0.35]].forEach(([ex,ey]) => {
        ctx.beginPath(); ctx.arc(ex,ey,4,0,Math.PI*2); ctx.fill();
      });
      ctx.shadowBlur = 0;
    }
  } else {
    // No face guide
    ctx.strokeStyle = 'rgba(239,68,68,0.4)';
    ctx.lineWidth   = 1.5;
    ctx.setLineDash([5,5]);
    ctx.strokeRect(60,20,180,185);
    ctx.setLineDash([]);
    ctx.fillStyle = 'rgba(239,68,68,0.6)';
    ctx.font = '11px Inter, sans-serif';
    ctx.fillText('Sin cara detectada — centra tu rostro', 20, 210);
  }
}

// ── NLP live ───────────────────────────────────────────
document.getElementById('comentario').addEventListener('input', function() {
  clearTimeout(nlpTimer);
  const text = this.value.trim();
  if (text.length < 8) {
    document.getElementById('nlpLive').innerHTML = '';
    document.getElementById('kwWrap').innerHTML  = '';
    return;
  }
  nlpTimer = setTimeout(() => doNLP(text), 500);
});

async function doNLP(text) {
  try {
    const res  = await fetch('/api/v1/nlp/analyze', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    const icons = { positivo:'😊', negativo:'😟', neutral:'😐' };
    const pct   = ((data.score||0)*100).toFixed(0);
    document.getElementById('nlpLive').innerHTML =
      `<span class="nlp-pill ${data.label}">${icons[data.label]||''}  ${(data.label||'').charAt(0).toUpperCase()+(data.label||'').slice(1)} (${pct}%)</span>`;
    document.getElementById('kwWrap').innerHTML =
      (data.keywords||[]).map(k=>`<span class="chip">${k}</span>`).join('');
  } catch(e) {}
}

// ── Resumen ─────────────────────────────────────────────
function buildResumen() {
  const emjs = {'1':'😞','2':'😕','3':'😐','4':'🙂','5':'😄'};
  const ejmap = {'1':'🤯','2':'😵','3':'🤔','4':'🧠','5':'💡'};
  const edmap = {'1':'👎','2':'😤','3':'😶','4':'👍','5':'🏆'};
  const cal = document.getElementById('calidad_clase').value;
  const com = document.getElementById('comprension_tema').value;
  const doc = document.getElementById('evaluacion_docente').value;
  const txt = document.getElementById('comentario').value;
  document.getElementById('resumen').innerHTML = `
    <div style="display:flex;flex-direction:column;gap:8px">
      <div class="flex justify-between"><span style="color:#64748B">Calidad de clase</span><b>${emjs[cal]||'—'} ${cal||'—'}/5</b></div>
      <div class="flex justify-between"><span style="color:#64748B">Comprensión</span><b>${ejmap[com]||'—'} ${com||'—'}/5</b></div>
      <div class="flex justify-between"><span style="color:#64748B">Docente</span><b>${edmap[doc]||'—'} ${doc||'—'}/5</b></div>
      ${txt?`<div style="margin-top:4px;padding:8px;background:#fff;border-radius:8px;font-size:12px;color:#475569;border:1px solid #E2E8F0">💬 "${txt.substring(0,100)}${txt.length>100?'...':''}"</div>`:''}
      ${emoCaptures.length?`<div style="font-size:12px;color:#64748B;margin-top:2px">📷 ${emoCaptures.length} capturas emocionales</div>`:''}
    </div>`;
}

// ── Submit ──────────────────────────────────────────────
async function submitSurvey() {
  const btn = document.getElementById('submitBtn');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Analizando con IA...';
  const payload = {
    survey_id:         document.getElementById('survey_id').value,
    student_id:        document.getElementById('student_id').value,
    calidad_clase:     document.getElementById('calidad_clase').value,
    comprension_tema:  document.getElementById('comprension_tema').value,
    evaluacion_docente:document.getElementById('evaluacion_docente').value,
    comentario:        document.getElementById('comentario').value,
    emotion_captures:  emoCaptures,
  };
  if (!payload.calidad_clase || !payload.comprension_tema || !payload.evaluacion_docente) {
    alert('Completa todas las preguntas antes de enviar.');
    btn.disabled=false; btn.innerHTML='<i class="fas fa-paper-plane"></i> Enviar encuesta';
    return;
  }
  try {
    const res  = await fetch('/survey/submit', {
      method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.status==='ok') {
      stopCam();
      if (localTrackTimer) clearInterval(localTrackTimer);
      document.getElementById('confirmCard').style.display  = 'none';
      document.getElementById('resultadoFinal').style.display = 'block';
      document.getElementById('prevBtn').style.display       = 'none';
      renderResultado(data.kpis);
    } else {
      throw new Error('Server error');
    }
  } catch(e) {
    alert('Error al enviar. Intenta de nuevo.');
    btn.disabled=false; btn.innerHTML='<i class="fas fa-paper-plane"></i> Enviar encuesta';
  }
}

function renderResultado(kpis) {
  const items = [
    {label:'Comprensión', val:kpis.indice_comprension,          color:'#4F46E5'},
    {label:'Atención',    val:kpis.indice_atencion,             color:'#06B6D4'},
    {label:'Nivelación',  val:kpis.indice_nivelacion,           color:'#10B981'},
    {label:'Coherencia',  val:kpis.indice_coherencia_emocional, color:'#F59E0B'},
  ];
  document.getElementById('resultKpis').innerHTML = items.map(i=>`
    <div class="result-kpi">
      <div class="result-val" style="color:${i.color}">${((i.val||0)*100).toFixed(1)}%</div>
      <div class="result-lbl">${i.label}</div>
    </div>`).join('');
  const r = kpis.riesgo_insatisfaccion || 'medio';
  const m = {bajo:['#D1FAE5','#065F46','🟢'],medio:['#FEF3C7','#92400E','🟡'],alto:['#FEE2E2','#991B1B','🔴']};
  const [bg,color,ic] = m[r]||m.medio;
  document.getElementById('resultRiesgo').innerHTML =
    `<div style="background:${bg};color:${color};padding:12px;border-radius:10px">${ic} Riesgo académico: <b>${r.toUpperCase()}</b></div>`;
}

// ── Init ───────────────────────────────────────────────
updateUI();
</script>
</body>
</html>
