@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --primary:       #4F46E5;
  --primary-light: #818CF8;
  --primary-dark:  #3730A3;
  --accent:        #06B6D4;
  --success:       #10B981;
  --warning:       #F59E0B;
  --danger:        #EF4444;
  --info:          #3B82F6;
  --bg:            #F8FAFC;
  --bg-card:       #FFFFFF;
  --text:          #0F172A;
  --text-muted:    #64748B;
  --border:        #E2E8F0;
  --radius:        14px;
  --radius-sm:     8px;
  --shadow:        0 1px 3px rgba(0,0,0,.08), 0 4px 16px rgba(0,0,0,.06);
  --shadow-lg:     0 8px 32px rgba(79,70,229,.15);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); font-family: 'Inter', system-ui, sans-serif; color: var(--text); font-size: 14px; }
a { color: var(--primary); text-decoration: none; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* ── SIDEBAR ── */
.sidebar {
  position: fixed; top: 0; left: 0; height: 100vh; width: 240px;
  background: linear-gradient(180deg, var(--primary-dark) 0%, var(--primary) 100%);
  display: flex; flex-direction: column; z-index: 100; overflow: hidden;
}
.sidebar-logo {
  padding: 24px 20px 20px;
  border-bottom: 1px solid rgba(255,255,255,.12);
  display: flex; align-items: center; gap: 12px;
}
.sidebar-logo .logo-icon {
  width: 36px; height: 36px; background: rgba(255,255,255,.2);
  border-radius: 10px; display: flex; align-items: center; justify-content: center;
  font-size: 18px;
}
.sidebar-logo span { font-size: 16px; font-weight: 700; color: #fff; }
.sidebar-logo small { display: block; font-size: 10px; color: rgba(255,255,255,.6); font-weight: 400; }
.sidebar-nav { flex: 1; padding: 16px 12px; overflow-y: auto; }
.nav-section-label {
  font-size: 10px; font-weight: 600; letter-spacing: .08em;
  color: rgba(255,255,255,.45); padding: 12px 8px 6px; text-transform: uppercase;
}
.nav-link {
  display: flex; align-items: center; gap: 10px; padding: 9px 12px;
  border-radius: var(--radius-sm); color: rgba(255,255,255,.75);
  font-size: 13px; font-weight: 500; transition: all .15s; margin-bottom: 2px;
}
.nav-link:hover, .nav-link.active {
  background: rgba(255,255,255,.15); color: #fff;
}
.nav-link i { width: 16px; text-align: center; font-size: 13px; }
.sidebar-footer {
  padding: 16px 12px; border-top: 1px solid rgba(255,255,255,.12);
}
.user-card {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px; border-radius: var(--radius-sm);
  background: rgba(255,255,255,.1);
}
.user-avatar {
  width: 32px; height: 32px; border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--primary-light));
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700; color: #fff; flex-shrink: 0;
}
.user-info .name { font-size: 12px; font-weight: 600; color: #fff; }
.user-info .role { font-size: 10px; color: rgba(255,255,255,.5); }

/* ── MAIN LAYOUT ── */
.main-wrap { margin-left: 240px; min-height: 100vh; display: flex; flex-direction: column; }
.topbar {
  position: sticky; top: 0; z-index: 50;
  background: rgba(248,250,252,.9); backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 0 28px; height: 60px; display: flex; align-items: center; justify-content: space-between;
}
.topbar-title { font-size: 15px; font-weight: 600; }
.topbar-actions { display: flex; align-items: center; gap: 12px; }
.page-content { padding: 28px; flex: 1; }

/* ── CARDS ── */
.card {
  background: var(--bg-card); border-radius: var(--radius);
  border: 1px solid var(--border); box-shadow: var(--shadow);
}
.card-header-clean {
  padding: 18px 20px 0; font-size: 14px; font-weight: 600;
}
.card-body-pad { padding: 20px; }

/* ── KPI CARDS ── */
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px,1fr)); gap: 16px; }
.kpi-card {
  background: var(--bg-card); border-radius: var(--radius);
  border: 1px solid var(--border); padding: 20px;
  position: relative; overflow: hidden; transition: transform .2s, box-shadow .2s;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }
.kpi-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
}
.kpi-card.indigo::before  { background: var(--primary); }
.kpi-card.cyan::before    { background: var(--accent); }
.kpi-card.emerald::before { background: var(--success); }
.kpi-card.amber::before   { background: var(--warning); }
.kpi-card.rose::before    { background: var(--danger); }
.kpi-icon {
  width: 40px; height: 40px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center; margin-bottom: 14px;
}
.kpi-icon.indigo  { background: #EEF2FF; color: var(--primary); }
.kpi-icon.cyan    { background: #ECFEFF; color: var(--accent); }
.kpi-icon.emerald { background: #ECFDF5; color: var(--success); }
.kpi-icon.amber   { background: #FFFBEB; color: var(--warning); }
.kpi-icon.rose    { background: #FFF1F2; color: var(--danger); }
.kpi-value { font-size: 28px; font-weight: 800; letter-spacing: -.5px; }
.kpi-label { font-size: 12px; color: var(--text-muted); font-weight: 500; margin-top: 2px; }
.kpi-delta { font-size: 11px; font-weight: 600; margin-top: 8px; }
.kpi-delta.up { color: var(--success); }
.kpi-delta.down { color: var(--danger); }

/* ── BADGE ── */
.badge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 8px; border-radius: 20px; font-size: 11px; font-weight: 600;
}
.badge-success { background: #D1FAE5; color: #065F46; }
.badge-warning { background: #FEF3C7; color: #92400E; }
.badge-danger  { background: #FEE2E2; color: #991B1B; }
.badge-info    { background: #DBEAFE; color: #1E40AF; }
.badge-neutral { background: #F1F5F9; color: #475569; }
.badge-primary { background: #EEF2FF; color: #3730A3; }

/* ── BUTTONS ── */
.btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 16px; border-radius: var(--radius-sm);
  font-size: 13px; font-weight: 600; border: none; cursor: pointer; transition: all .15s;
}
.btn-primary { background: var(--primary); color: #fff; }
.btn-primary:hover { background: var(--primary-dark); transform: translateY(-1px); }
.btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text); }
.btn-outline:hover { background: var(--bg); border-color: var(--primary); color: var(--primary); }
.btn-success { background: var(--success); color: #fff; }
.btn-danger  { background: var(--danger); color: #fff; }
.btn-ghost   { background: transparent; color: var(--text-muted); }
.btn-ghost:hover { background: var(--bg); color: var(--text); }
.btn-lg { padding: 12px 24px; font-size: 15px; border-radius: var(--radius); }
.btn-sm { padding: 5px 10px; font-size: 12px; }
.btn:disabled { opacity: .5; cursor: not-allowed; transform: none !important; }

/* ── FORM CONTROLS ── */
.form-group { margin-bottom: 18px; }
.form-label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 6px; color: var(--text); }
.form-hint  { font-size: 11px; color: var(--text-muted); margin-top: 4px; }
.form-control {
  width: 100%; padding: 9px 12px; border: 1.5px solid var(--border);
  border-radius: var(--radius-sm); font-size: 13px; font-family: inherit;
  background: var(--bg-card); color: var(--text); transition: border-color .15s, box-shadow .15s;
  outline: none;
}
.form-control:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(79,70,229,.1); }
textarea.form-control { resize: vertical; min-height: 90px; }

/* ── PROGRESS BAR ── */
.progress-bar-wrap {
  background: var(--border); border-radius: 20px; height: 8px; overflow: hidden;
}
.progress-bar-fill {
  height: 100%; border-radius: 20px; transition: width .6s cubic-bezier(.4,0,.2,1);
}

/* ── LOGIN ── */
.login-page {
  min-height: 100vh; display: flex;
  background: linear-gradient(135deg, #EEF2FF 0%, #E0F2FE 50%, #F0FDF4 100%);
}
.login-left {
  flex: 1; display: flex; flex-direction: column; justify-content: center;
  padding: 60px; background: linear-gradient(160deg, var(--primary-dark) 0%, var(--primary) 60%, var(--accent) 100%);
}
.login-left h1 { font-size: 38px; font-weight: 800; color: #fff; line-height: 1.15; margin-bottom: 16px; }
.login-left p  { font-size: 15px; color: rgba(255,255,255,.7); max-width: 380px; line-height: 1.6; }
.login-feature { display: flex; align-items: center; gap: 12px; margin-top: 20px; }
.login-feature-icon {
  width: 36px; height: 36px; border-radius: 10px;
  background: rgba(255,255,255,.15); display: flex; align-items: center; justify-content: center; color: #fff; font-size: 14px;
}
.login-feature span { font-size: 13px; color: rgba(255,255,255,.8); }
.login-right { flex: 1; display: flex; align-items: center; justify-content: center; padding: 40px; }
.login-box { width: 100%; max-width: 400px; }
.login-box h2 { font-size: 24px; font-weight: 700; margin-bottom: 6px; }
.login-box .sub { font-size: 13px; color: var(--text-muted); margin-bottom: 32px; }
.input-icon-wrap { position: relative; }
.input-icon-wrap i { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: var(--text-muted); font-size: 13px; }
.input-icon-wrap .form-control { padding-left: 36px; }

/* ── SURVEY ── */
.survey-page { max-width: 720px; margin: 0 auto; padding: 24px 16px 60px; }
.survey-progress-bar {
  position: sticky; top: 0; z-index: 40; background: var(--bg);
  padding: 12px 0; margin-bottom: 24px;
}
.survey-step { display: none; }
.survey-step.active { display: block; animation: fadeSlide .3s ease; }
@keyframes fadeSlide { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }

.rating-row { display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; }
.rating-btn {
  flex: 1; min-width: 52px; padding: 14px 8px;
  border: 1.5px solid var(--border); border-radius: var(--radius);
  background: var(--bg-card); cursor: pointer; text-align: center;
  font-size: 13px; font-weight: 600; color: var(--text-muted); transition: all .15s;
  display: flex; flex-direction: column; align-items: center; gap: 4px;
}
.rating-btn:hover { border-color: var(--primary); color: var(--primary); background: #EEF2FF; }
.rating-btn.selected { border-color: var(--primary); background: var(--primary); color: #fff; }
.rating-btn .star { font-size: 18px; }
.rating-btn .label { font-size: 10px; font-weight: 500; }

/* ── CAMERA CARD ── */
.camera-card {
  border: 2px dashed var(--border); border-radius: var(--radius);
  padding: 24px; text-align: center; transition: all .2s;
}
.camera-card.active { border-color: var(--success); border-style: solid; background: #F0FDF4; }
.camera-preview-wrap {
  position: relative; display: inline-block; border-radius: var(--radius); overflow: hidden;
}
#videoFeed { display: block; border-radius: var(--radius); }
.emotion-overlay {
  position: absolute; bottom: 8px; left: 8px; right: 8px;
  background: rgba(0,0,0,.65); backdrop-filter: blur(4px);
  border-radius: 8px; padding: 6px 10px;
  display: flex; align-items: center; gap: 8px; justify-content: space-between;
}
.emotion-label { font-size: 12px; font-weight: 600; color: #fff; }
.emotion-bars { display: flex; gap: 4px; align-items: flex-end; height: 24px; }
.emotion-bar { width: 6px; border-radius: 3px; background: rgba(255,255,255,.3); transition: height .4s; min-height: 3px; }
.emotion-bar.feliz     { background: #34D399; }
.emotion-bar.neutral   { background: #94A3B8; }
.emotion-bar.triste    { background: #60A5FA; }
.emotion-bar.enojado   { background: #F87171; }
.emotion-bar.sorprendido { background: #FBBF24; }

/* ── NLP LIVE ── */
.nlp-live {
  margin-top: 10px; padding: 12px 14px;
  border-radius: var(--radius-sm); border: 1px solid var(--border);
  background: var(--bg); font-size: 12px; min-height: 50px; transition: all .3s;
}
.nlp-live.positivo { border-color: var(--success); background: #F0FDF4; }
.nlp-live.negativo { border-color: var(--danger); background: #FFF1F2; }
.nlp-live.neutral  { border-color: var(--border); }

/* ── HISTORIAL TABLE ── */
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th { text-align: left; padding: 10px 14px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .05em; color: var(--text-muted); border-bottom: 1px solid var(--border); background: var(--bg); }
.data-table td { padding: 12px 14px; border-bottom: 1px solid var(--border); }
.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover td { background: var(--bg); }

/* ── EMOTION PIE ── */
.emotion-pill {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;
}
.emotion-pill.feliz     { background: #D1FAE5; color: #065F46; }
.emotion-pill.neutral   { background: #F1F5F9; color: #475569; }
.emotion-pill.triste    { background: #DBEAFE; color: #1E40AF; }
.emotion-pill.enojado   { background: #FEE2E2; color: #991B1B; }
.emotion-pill.sorprendido { background: #FEF3C7; color: #92400E; }

/* ── RESPONSIVE ── */
@media (max-width: 900px) {
  .sidebar { width: 60px; }
  .sidebar-logo span, .sidebar-logo small, .nav-section-label, .nav-link span, .user-info { display: none; }
  .sidebar-logo { justify-content: center; }
  .nav-link { justify-content: center; }
  .main-wrap { margin-left: 60px; }
  .login-left { display: none; }
}
@media (max-width: 600px) {
  .page-content { padding: 16px; }
  .kpi-grid { grid-template-columns: 1fr 1fr; }
}

/* ── MISC ── */
.divider { border: none; border-top: 1px solid var(--border); margin: 20px 0; }
.text-muted { color: var(--text-muted); }
.text-sm { font-size: 12px; }
.fw-600 { font-weight: 600; }
.fw-700 { font-weight: 700; }
.mb-0 { margin-bottom: 0; }
.mb-4 { margin-bottom: 4px; }
.mb-8 { margin-bottom: 8px; }
.mb-16 { margin-bottom: 16px; }
.mb-24 { margin-bottom: 24px; }
.gap-8  { gap: 8px; }
.gap-12 { gap: 12px; }
.gap-16 { gap: 16px; }
.flex { display: flex; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.w-full { width: 100%; }
.text-center { text-align: center; }
.rounded { border-radius: var(--radius); }
.spinner {
  width: 20px; height: 20px; border: 2px solid rgba(255,255,255,.3);
  border-top-color: #fff; border-radius: 50%; animation: spin .7s linear infinite; display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }
.blink { animation: blink 1s ease-in-out infinite; }
@keyframes blink { 0%,100% { opacity: 1; } 50% { opacity: .3; } }
.chip {
  display: inline-flex; align-items: center; padding: 2px 8px;
  background: var(--bg); border: 1px solid var(--border); border-radius: 20px;
  font-size: 11px; color: var(--text-muted); margin: 2px;
}

/* ── E2E-BI BAR IN SIDEBAR ── */
.e2e-bar {
  margin: 0 12px 4px;
  padding: 10px 10px 12px;
  background: rgba(255,255,255,.08);
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,.1);
}
.e2e-bar-label {
  font-size: 9px; font-weight: 700; letter-spacing: .1em;
  color: rgba(255,255,255,.4); margin-bottom: 8px; text-align: center;
}
.e2e-steps-mini {
  display: flex; align-items: center; justify-content: center;
  gap: 2px; flex-wrap: nowrap;
}
.e2e-mini {
  display: flex; flex-direction: column; align-items: center;
  text-decoration: none; gap: 3px;
}
.e2e-mini:hover .e2e-dot { transform: scale(1.2); }
.e2e-dot {
  width: 20px; height: 20px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 9px; font-weight: 800; color: #fff;
  transition: transform .15s; flex-shrink: 0;
}
.e2e-mini-lbl {
  font-size: 8px; color: rgba(255,255,255,.55); font-weight: 600;
  white-space: nowrap;
}
.e2e-arrow {
  color: rgba(255,255,255,.25); font-size: 12px; line-height: 1;
  margin-bottom: 12px; flex-shrink: 0;
}

/* ── E2E STEP CARDS ON PIPELINE PAGE ── */
.e2e-step:hover {
  background: rgba(79,70,229,.06) !important;
  border-color: var(--primary) !important;
  transform: translateY(-2px);
}

/* ── RESPONSIVE SIDEBAR COLLAPSE ── */
@media (max-width: 900px) {
  .sidebar { width: 60px; }
  .sidebar-logo span, .sidebar-logo small,
  .nav-section-label, .nav-link span,
  .user-info, .e2e-bar-label, .e2e-mini-lbl, .e2e-arrow { display: none; }
  .sidebar-logo { justify-content: center; }
  .nav-link { justify-content: center; }
  .main-wrap { margin-left: 60px; }
  .e2e-steps-mini { flex-direction: column; gap: 4px; }
  .e2e-bar { padding: 8px 6px; }
}
