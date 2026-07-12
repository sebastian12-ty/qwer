const rmap={student:'badge-info',teacher:'badge-primary',coordinator:'badge-warning',admin:'badge-danger'};

// ── Usuarios ────────────────────────────────────────────
let allUsers=[];
async function loadAdminUsers(){
  const data=await fetch('/api/v1/admin/users').then(r=>r.json()).catch(()=>({users:[]}));
  allUsers=data.users||[];
  renderUsers(allUsers);
}
function renderUsers(rows){
  const tbody=document.getElementById('usersBody');
  if(!tbody)return;
  tbody.innerHTML=rows.length?rows.map(u=>`<tr>
    <td style="font-size:12px">${u.email}</td>
    <td><span class="badge ${rmap[u.role]||'badge-neutral'}">${u.role}</span></td>
    <td><span class="badge ${u.active?'badge-success':'badge-neutral'}">${u.active?'Activo':'Inactivo'}</span></td>
    <td style="font-size:11px;color:#94A3B8">${u.created_at?new Date(u.created_at).toLocaleDateString('es-PE'):''}</td>
    <td><button class="btn btn-ghost btn-sm" onclick="toggleUser(${u.id})" title="${u.active?'Desactivar':'Activar'}">
      <i class="fas fa-toggle-${u.active?'on text-success':'off'}"></i>
    </button></td>
  </tr>`).join(''):'<tr><td colspan="5" style="text-align:center;padding:20px;color:#94A3B8">Sin usuarios</td></tr>';
  // Filter binding
  ['searchUser','filterRole'].forEach(id=>{
    const el=document.getElementById(id);
    if(el) el.addEventListener('input',()=>filterUsers());
  });
}
function filterUsers(){
  const q=(document.getElementById('searchUser')?.value||'').toLowerCase();
  const r=document.getElementById('filterRole')?.value||'';
  renderUsers(allUsers.filter(u=>(!q||u.email.toLowerCase().includes(q))&&(!r||u.role===r)));
}
async function toggleUser(id){
  await fetch(`/api/v1/admin/users/${id}/toggle`,{method:'POST'});
  loadAdminUsers();
}
async function crearUsuario(){
  const email=document.getElementById('new-email')?.value.trim();
  const pw=document.getElementById('new-password')?.value;
  const role=document.getElementById('new-role')?.value;
  const err=document.getElementById('user-error');
  if(err)err.style.display='none';
  if(!email||!pw){if(err){err.textContent='Completa todos los campos.';err.style.display='block';}return;}
  const data=await fetch('/api/v1/admin/users',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({email,password:pw,role})}).then(r=>r.json()).catch(()=>({error:'Error de red'}));
  if(data.error){if(err){err.textContent=data.error;err.style.display='block';}return;}
  document.getElementById('userModal').style.display='none';
  loadAdminUsers();
}

// ── Docentes ────────────────────────────────────────────
async function loadDocentes(){
  const [users,surveys]=await Promise.all([
    fetch('/api/v1/admin/users').then(r=>r.json()).catch(()=>({users:[]})),
    fetch('/api/v1/teacher/encuestas').then(r=>r.json()).catch(()=>({surveys:[]})),
  ]);
  const teachers=(users.users||[]).filter(u=>u.role==='teacher');
  const surveysByTeacher={};
  (surveys.surveys||[]).forEach(s=>{
    if(!surveysByTeacher[s.teacher_id]) surveysByTeacher[s.teacher_id]={count:0,resp:0};
    surveysByTeacher[s.teacher_id].count++;
    surveysByTeacher[s.teacher_id].resp+=(s.respuestas||0);
  });
  const tbody=document.getElementById('docentes-body');
  if(!tbody)return;
  const data=await fetch('/api/v1/admin/teachers').then(r=>r.json()).catch(()=>({teachers:[]}));
  tbody.innerHTML=(data.teachers||[]).length?(data.teachers||[]).map(t=>{
    const sd=surveysByTeacher[t.id]||{count:0,resp:0};
    return `<tr>
      <td style="font-weight:600">${t.nombre}</td>
      <td style="font-size:12px">${t.email||'—'}</td>
      <td style="font-size:12px">${t.especialidad||'—'}</td>
      <td>${t.n_cursos||0}</td>
      <td>${sd.count}</td>
      <td>${sd.resp}</td>
    </tr>`;
  }).join(''):'<tr><td colspan="6" style="text-align:center;padding:24px;color:#94A3B8">Sin docentes registrados</td></tr>';
}
async function crearDocente(){
  const email=document.getElementById('doc-email')?.value.trim();
  const pw=document.getElementById('doc-pass')?.value;
  const nombre=document.getElementById('doc-nombre')?.value.trim();
  const esp=document.getElementById('doc-esp')?.value.trim();
  const dep=document.getElementById('doc-dep')?.value.trim();
  const err=document.getElementById('doc-error');
  if(err)err.style.display='none';
  if(!email||!pw||!nombre){if(err){err.textContent='Email, contraseña y nombre son requeridos.';err.style.display='block';}return;}
  const data=await fetch('/api/v1/admin/teachers',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({email,password:pw,nombre,especialidad:esp,departamento:dep})
  }).then(r=>r.json()).catch(()=>({error:'Error de red'}));
  if(data.error){if(err){err.textContent=data.error;err.style.display='block';}return;}
  document.getElementById('docModal').style.display='none';
  loadDocentes();
}

// ── Cursos ──────────────────────────────────────────────
async function loadCursos(){
  const data=await fetch('/api/v1/admin/courses').then(r=>r.json()).catch(()=>({courses:[]}));
  const tbody=document.getElementById('cursos-body');
  if(!tbody)return;
  tbody.innerHTML=(data.courses||[]).length?(data.courses||[]).map(c=>`<tr>
    <td><code style="background:#EEF2FF;color:#4F46E5;padding:2px 6px;border-radius:4px;font-size:11px">${c.codigo}</code></td>
    <td style="font-weight:600">${c.nombre}</td>
    <td>${c.carrera}</td>
    <td style="text-align:center">${c.creditos}</td>
    <td style="text-align:center">${c.n_surveys||0}</td>
  </tr>`).join(''):'<tr><td colspan="5" style="text-align:center;padding:24px;color:#94A3B8">Sin cursos registrados</td></tr>';
}
async function crearCurso(){
  const codigo=document.getElementById('c-codigo')?.value.trim().toUpperCase();
  const nombre=document.getElementById('c-nombre')?.value.trim();
  const carrera=document.getElementById('c-carrera')?.value.trim();
  const creditos=parseInt(document.getElementById('c-creditos')?.value)||4;
  const err=document.getElementById('curso-error');
  if(err)err.style.display='none';
  if(!codigo||!nombre||!carrera){if(err){err.textContent='Completa todos los campos.';err.style.display='block';}return;}
  const data=await fetch('/api/v1/admin/courses',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({codigo,nombre,carrera,creditos})
  }).then(r=>r.json()).catch(()=>({error:'Error de red'}));
  if(data.error){if(err){err.textContent=data.error;err.style.display='block';}return;}
  document.getElementById('cursoModal').style.display='none';
  loadCursos();
}

// ── Admin dashboard ─────────────────────────────────────
async function loadAdmin(){
  const [stats,users,surveys]=await Promise.all([
    fetch('/api/v1/admin/stats').then(r=>r.json()).catch(()=>({})),
    fetch('/api/v1/admin/users').then(r=>r.json()).catch(()=>({users:[]})),
    fetch('/api/v1/admin/surveys').then(r=>r.json()).catch(()=>({surveys:[]})),
  ]);
  const set=(id,v)=>{const el=document.getElementById(id);if(el)el.textContent=v;};
  set('a-users',stats.users??'—'); set('a-surveys',stats.surveys??'—');
  set('a-responses',stats.responses??'—'); set('a-students',stats.students??'—');
  set('a-teachers',stats.teachers??'—'); set('a-captures',stats.captures??'—');
  const tbody=document.getElementById('usersBody');
  if(tbody){
    tbody.innerHTML=(users.users||[]).map(u=>`<tr>
      <td style="font-size:12px">${u.email}</td>
      <td><span class="badge ${rmap[u.role]||'badge-neutral'}">${u.role}</span></td>
      <td><span class="badge ${u.active?'badge-success':'badge-neutral'}">${u.active?'Activo':'Inactivo'}</span></td>
      <td><button class="btn btn-ghost btn-sm" onclick="toggleUser(${u.id})"><i class="fas fa-toggle-${u.active?'on text-success':'off'}"></i></button></td>
    </tr>`).join('')||'<tr><td colspan="4" style="text-align:center;padding:20px;color:#94A3B8">Sin usuarios</td></tr>';
  }
  const sbody=document.getElementById('surveysBody');
  if(sbody){
    sbody.innerHTML=(surveys.surveys||[]).map(s=>`<tr>
      <td style="font-size:12px;font-weight:500">${s.titulo}</td>
      <td><code style="background:#EEF2FF;color:#4F46E5;padding:2px 6px;border-radius:4px;font-size:11px">${s.codigo_qr}</code></td>
      <td><span class="badge ${s.activa?'badge-success':'badge-neutral'}">${s.activa?'Sí':'No'}</span></td>
      <td><a href="/survey/${s.codigo_qr}" target="_blank" class="btn btn-ghost btn-sm"><i class="fas fa-external-link-alt"></i></a></td>
    </tr>`).join('')||'<tr><td colspan="4" style="text-align:center;padding:20px;color:#94A3B8">Sin encuestas</td></tr>';
  }
}
