{% extends "base.html" %}
{% block title %}Modelo Estrella{% endblock %}
{% block page_title %}Diagrama Modelo Estrella — En Vivo{% endblock %}
{% block topbar_actions %}
  <span id="last-update" style="font-size:11px;color:#64748B"></span>
  <span id="auto-badge" class="badge badge-success"><i class="fas fa-circle blink"></i> Auto-actualizando</span>
{% endblock %}
{% block content %}
<div class="card" style="padding:24px">
  <canvas id="starCanvas" style="width:100%;max-width:900px;display:block;margin:0 auto"></canvas>
</div>

<!-- Stats debajo -->
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-top:16px" id="star-stats"></div>
{% endblock %}
{% block scripts %}
<script>
const COLORS = {
  fact: '#4F46E5', dim1:'#06B6D4', dim2:'#10B981', dim3:'#F59E0B', dim4:'#8B5CF6', dim5:'#EF4444'
};

let schema = null;

async function loadSchema() {
  try {
    schema = await fetch('/bi/star-schema').then(r=>r.json());
    draw();
    renderStats();
    document.getElementById('last-update').textContent =
      'Actualizado: ' + new Date().toLocaleTimeString('es-PE');
  } catch(e) { console.error(e); }
}

function draw() {
  const canvas = document.getElementById('starCanvas');
  const dpr = window.devicePixelRatio || 1;
  const W = canvas.offsetWidth || 900;
  const H = 480;
  canvas.width  = W * dpr;
  canvas.height = H * dpr;
  canvas.style.height = H + 'px';
  const ctx = canvas.getContext('2d');
  ctx.scale(dpr, dpr);

  ctx.clearRect(0, 0, W, H);
  const cx = W/2, cy = H/2;

  const dims = schema.dimensions;
  const angleStep = (Math.PI * 2) / dims.length;
  const r = Math.min(W, H) * 0.33;

  // Draw lines from fact to each dim
  dims.forEach((dim, i) => {
    const angle = -Math.PI/2 + angleStep * i;
    const dx = cx + r * Math.cos(angle);
    const dy = cy + r * Math.sin(angle);
    ctx.beginPath();
    ctx.setLineDash([6, 4]);
    ctx.moveTo(cx, cy);
    ctx.lineTo(dx, dy);
    ctx.strokeStyle = '#CBD5E1';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.setLineDash([]);
    // FK arrow
    drawArrow(ctx, dx, dy, cx, cy, '#CBD5E1');
  });

  // Draw dim boxes
  dims.forEach((dim, i) => {
    const angle = -Math.PI/2 + angleStep * i;
    const dx = cx + r * Math.cos(angle);
    const dy = cy + r * Math.sin(angle);
    const color = Object.values(COLORS)[i+1] || '#64748B';
    drawBox(ctx, dx, dy, dim.name, dim.rows, dim.fields, color, 130, 80);
  });

  // Draw fact center (bigger)
  drawBox(ctx, cx, cy, schema.fact.name, schema.fact.rows, schema.fact.fields, COLORS.fact, 160, 100, true);
}

function drawBox(ctx, x, y, title, rows, fields, color, w, h, isFact=false) {
  const bx = x - w/2, by = y - h/2;
  // Shadow
  ctx.shadowColor = color + '40';
  ctx.shadowBlur = 12;
  // Box
  ctx.fillStyle = isFact ? color : '#fff';
  roundRect(ctx, bx, by, w, h, 10);
  ctx.fill();
  ctx.shadowBlur = 0;
  // Border
  ctx.strokeStyle = color;
  ctx.lineWidth = isFact ? 0 : 2;
  if (!isFact) { roundRect(ctx, bx, by, w, h, 10); ctx.stroke(); }
  // Header bar
  if (!isFact) {
    ctx.fillStyle = color;
    roundRect(ctx, bx, by, w, 26, 10, true);
    ctx.fill();
  }
  // Title
  ctx.fillStyle = '#fff';
  ctx.font = `bold ${isFact?13:11}px Inter, sans-serif`;
  ctx.textAlign = 'center';
  ctx.fillText(title, x, by + (isFact ? 20 : 17));
  // Rows
  ctx.fillStyle = isFact ? 'rgba(255,255,255,.7)' : color;
  ctx.font = `${isFact?11:10}px Inter, sans-serif`;
  ctx.fillText(`${rows?.toLocaleString()} filas`, x, by + (isFact ? 36 : 36));
  // Fields
  ctx.fillStyle = isFact ? 'rgba(255,255,255,.6)' : '#64748B';
  ctx.font = '9px Inter, sans-serif';
  const ftext = (fields||[]).slice(0,3).join(', ') + (fields?.length>3?'...':'');
  ctx.fillText(ftext, x, by + (isFact ? 52 : 52));
}

function drawArrow(ctx, fromX, fromY, toX, toY, color) {
  const angle = Math.atan2(toY-fromY, toX-fromX);
  const len = 10;
  const ex = fromX + (toX-fromX)*0.35, ey = fromY + (toY-fromY)*0.35;
  ctx.beginPath();
  ctx.moveTo(ex, ey);
  ctx.lineTo(ex - len*Math.cos(angle-Math.PI/6), ey - len*Math.sin(angle-Math.PI/6));
  ctx.lineTo(ex - len*Math.cos(angle+Math.PI/6), ey - len*Math.sin(angle+Math.PI/6));
  ctx.closePath();
  ctx.fillStyle = color;
  ctx.fill();
}

function roundRect(ctx, x, y, w, h, r, topOnly=false) {
  ctx.beginPath();
  ctx.moveTo(x+r, y);
  ctx.arcTo(x+w, y, x+w, y+h, r);
  if (topOnly) { ctx.lineTo(x+w, y+h); ctx.lineTo(x, y+h); }
  else ctx.arcTo(x+w, y+h, x, y+h, r);
  ctx.arcTo(x, y+h, x, y, topOnly?0:r);
  ctx.arcTo(x, y, x+w, y, r);
  ctx.closePath();
}

function renderStats() {
  const all = [schema.fact, ...(schema.dimensions||[])];
  const colors = Object.values(COLORS);
  document.getElementById('star-stats').innerHTML = all.map((d,i)=>`
    <div class="card" style="padding:16px;text-align:center;border-top:3px solid ${colors[i]||'#64748B'}">
      <div style="font-size:18px;font-weight:800;color:${colors[i]||'#64748B'}">${(d.rows||0).toLocaleString()}</div>
      <div style="font-size:11px;color:#64748B;margin-top:3px">${d.name}</div>
    </div>`).join('');
}

// Auto-refresh every 15s
document.addEventListener('DOMContentLoaded', () => {
  loadSchema();
  setInterval(loadSchema, 15000);
});

window.addEventListener('resize', () => { if(schema) draw(); });
</script>
{% endblock %}
