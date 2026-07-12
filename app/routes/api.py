from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models.models import SurveyResponse, Survey, User, Student, Teacher, Course, EmotionCapture
from app.services.nlp_service import analyze_sentiment
from sqlalchemy import func
import uuid

api_bp = Blueprint('api', __name__)

# ── KPIs generales ──────────────────────────────────────────────────
@api_bp.route('/kpis/general')
@login_required
def kpis_general():
    r = db.session.query(
        func.avg(SurveyResponse.indice_comprension).label('comprension'),
        func.avg(SurveyResponse.indice_atencion).label('atencion'),
        func.avg(SurveyResponse.indice_coherencia_emocional).label('coherencia'),
        func.avg(SurveyResponse.indice_nivelacion).label('nivelacion'),
        func.avg(SurveyResponse.sentimiento_score).label('satisfaccion'),
        func.count(SurveyResponse.id).label('total'),
    ).first()
    return jsonify({
        'comprension':   round(float(r.comprension  or 0), 3),
        'atencion':      round(float(r.atencion     or 0), 3),
        'coherencia':    round(float(r.coherencia   or 0), 3),
        'nivelacion':    round(float(r.nivelacion   or 0), 3),
        'satisfaccion':  round(float(r.satisfaccion or 0), 3),
        'total_respuestas': r.total,
    })

@api_bp.route('/kpis/emociones')
@login_required
def kpis_emociones():
    r = db.session.query(
        func.avg(SurveyResponse.emocion_feliz).label('feliz'),
        func.avg(SurveyResponse.emocion_neutral).label('neutral'),
        func.avg(SurveyResponse.emocion_triste).label('triste'),
        func.avg(SurveyResponse.emocion_enojado).label('enojado'),
        func.avg(SurveyResponse.emocion_sorprendido).label('sorprendido'),
    ).first()
    return jsonify({k: round(float(getattr(r, k) or 0), 3)
                    for k in ['feliz','neutral','triste','enojado','sorprendido']})

@api_bp.route('/kpis/riesgo')
@login_required
def kpis_riesgo():
    return jsonify({
        'alto':  SurveyResponse.query.filter_by(riesgo_insatisfaccion='alto').count(),
        'medio': SurveyResponse.query.filter_by(riesgo_insatisfaccion='medio').count(),
        'bajo':  SurveyResponse.query.filter_by(riesgo_insatisfaccion='bajo').count(),
    })

# ── NLP en tiempo real ───────────────────────────────────────────────
@api_bp.route('/nlp/analyze', methods=['POST'])
def nlp_analyze():
    text = (request.get_json(force=True) or {}).get('text', '')
    score, label, keywords = analyze_sentiment(text)
    return jsonify({'score': score, 'label': label, 'keywords': keywords[:10]})

# ── Historial estudiante ─────────────────────────────────────────────
@api_bp.route('/student/historial')
@login_required
def student_historial():
    limit = min(int(request.args.get('limit', 20)), 200)
    rows = (
        db.session.query(SurveyResponse, Survey, Course, Teacher)
        .join(Survey,  SurveyResponse.survey_id  == Survey.id)
        .join(Course,  Survey.course_id           == Course.id)
        .join(Teacher, Survey.teacher_id          == Teacher.id)
        .order_by(SurveyResponse.fecha.desc())
        .limit(limit).all()
    )
    out = []
    for resp, survey, course, teacher in rows:
        out.append({
            'id':                      resp.id,
            'fecha':                   resp.fecha.isoformat(),
            'curso':                   course.nombre,
            'docente':                 teacher.nombre,
            'calidad_clase':           resp.calidad_clase,
            'comprension_tema':        resp.comprension_tema,
            'evaluacion_docente':      resp.evaluacion_docente,
            'comentario':              resp.comentario,
            'sentimiento_score':       resp.sentimiento_score,
            'sentimiento_label':       resp.sentimiento_label,
            'nlp_keywords':            resp.nlp_keywords or [],
            'emocion_predominante':    resp.emocion_predominante,
            'emocion_feliz':           resp.emocion_feliz,
            'emocion_neutral':         resp.emocion_neutral,
            'emocion_triste':          resp.emocion_triste,
            'emocion_enojado':         resp.emocion_enojado,
            'emocion_sorprendido':     resp.emocion_sorprendido,
            'indice_comprension':      resp.indice_comprension,
            'indice_atencion':         resp.indice_atencion,
            'indice_coherencia_emocional': resp.indice_coherencia_emocional,
            'indice_nivelacion':       resp.indice_nivelacion,
            'riesgo_insatisfaccion':   resp.riesgo_insatisfaccion,
        })
    return jsonify({'rows': out, 'total': len(out)})

# ── Encuestas del docente ────────────────────────────────────────────
@api_bp.route('/teacher/encuestas')
@login_required
def teacher_encuestas():
    rows = (
        db.session.query(
            Survey,
            func.count(SurveyResponse.id).label('respuestas'),
            func.avg(SurveyResponse.indice_nivelacion).label('nivelacion_prom'),
            func.avg(SurveyResponse.indice_comprension).label('comprension_prom'),
        )
        .outerjoin(SurveyResponse, SurveyResponse.survey_id == Survey.id)
        .group_by(Survey.id)
        .order_by(Survey.id.desc())
        .all()
    )
    return jsonify({'surveys': [{
        'id':             s.id,
        'titulo':         s.titulo,
        'codigo_qr':      s.codigo_qr,
        'activa':         s.activa,
        'respuestas':     r or 0,
        'nivelacion_prom':  round(float(n), 3) if n else None,
        'comprension_prom': round(float(c), 3) if c else None,
    } for s, r, n, c in rows]})

# ── Resultados por encuesta (para docente) ───────────────────────────
@api_bp.route('/teacher/encuesta/<int:survey_id>/resultados')
@login_required
def encuesta_resultados(survey_id):
    rows = (
        db.session.query(SurveyResponse, Student)
        .join(Student, SurveyResponse.student_id == Student.id)
        .filter(SurveyResponse.survey_id == survey_id)
        .order_by(SurveyResponse.fecha.desc())
        .all()
    )
    out = []
    for resp, student in rows:
        out.append({
            'id':                   resp.id,
            'estudiante':           student.nombre,
            'codigo':               student.codigo,
            'fecha':                resp.fecha.isoformat(),
            'calidad_clase':        resp.calidad_clase,
            'comprension_tema':     resp.comprension_tema,
            'evaluacion_docente':   resp.evaluacion_docente,
            'emocion_predominante': resp.emocion_predominante,
            'sentimiento_label':    resp.sentimiento_label,
            'indice_nivelacion':    resp.indice_nivelacion,
            'indice_comprension':   resp.indice_comprension,
            'riesgo_insatisfaccion':resp.riesgo_insatisfaccion,
            'comentario':           resp.comentario,
        })
    return jsonify({'rows': out, 'total': len(out)})

# ── Crear encuesta ───────────────────────────────────────────────────
@api_bp.route('/survey/create', methods=['POST'])
@login_required
def create_survey():
    data = request.get_json(force=True) or {}
    s = Survey(
        titulo=data.get('titulo', 'Sin título'),
        codigo_qr=str(uuid.uuid4())[:8].upper(),
        teacher_id=int(data.get('teacher_id', 1)),
        course_id=int(data.get('course_id', 1)),
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({'id': s.id, 'codigo_qr': s.codigo_qr})

@api_bp.route('/survey/<int:survey_id>/toggle', methods=['POST'])
@login_required
def toggle_survey(survey_id):
    s = Survey.query.get_or_404(survey_id)
    s.activa = not s.activa
    db.session.commit()
    return jsonify({'activa': s.activa})

# ── Admin: usuarios ──────────────────────────────────────────────────
@api_bp.route('/admin/users')
@login_required
def admin_users():
    users = User.query.order_by(User.id).all()
    return jsonify({'users': [
        {'id': u.id, 'email': u.email, 'role': u.role, 'active': u.active,
         'created_at': u.created_at.isoformat()}
        for u in users
    ]})

@api_bp.route('/admin/users/<int:uid>/toggle', methods=['POST'])
@login_required
def toggle_user(uid):
    u = User.query.get_or_404(uid)
    u.active = not u.active
    db.session.commit()
    return jsonify({'active': u.active})

@api_bp.route('/admin/users', methods=['POST'])
@login_required
def create_user():
    data = request.get_json(force=True) or {}
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'El email ya existe'}), 400
    u = User(email=data['email'], role=data.get('role', 'student'), active=True)
    u.set_password(data.get('password', 'changeme123'))
    db.session.add(u)
    db.session.commit()
    return jsonify({'id': u.id, 'email': u.email})

# ── Admin: encuestas ─────────────────────────────────────────────────
@api_bp.route('/admin/surveys')
@login_required
def admin_surveys():
    surveys = Survey.query.order_by(Survey.id.desc()).all()
    return jsonify({'surveys': [
        {'id': s.id, 'titulo': s.titulo, 'codigo_qr': s.codigo_qr,
         'activa': s.activa, 'created_at': s.created_at.isoformat()}
        for s in surveys
    ]})

# ── Admin: stats ─────────────────────────────────────────────────────
@api_bp.route('/admin/stats')
@login_required
def admin_stats():
    return jsonify({
        'users':     User.query.count(),
        'surveys':   Survey.query.count(),
        'responses': SurveyResponse.query.count(),
        'students':  Student.query.count(),
        'teachers':  Teacher.query.count(),
        'captures':  EmotionCapture.query.count(),
    })

# ── Exportar CSV ─────────────────────────────────────────────────────
@api_bp.route('/export/csv')
@login_required
def export_csv():
    import csv, io
    from flask import Response
    rows = (
        db.session.query(SurveyResponse, Survey, Course, Teacher, Student)
        .join(Survey,  SurveyResponse.survey_id  == Survey.id)
        .join(Course,  Survey.course_id           == Course.id)
        .join(Teacher, Survey.teacher_id          == Teacher.id)
        .join(Student, SurveyResponse.student_id  == Student.id)
        .order_by(SurveyResponse.fecha.desc())
        .all()
    )
    si = io.StringIO()
    w = csv.writer(si)
    w.writerow(['fecha','estudiante','curso','docente','calidad','comprension_encuesta',
                'evaluacion_docente','comentario','sentimiento','emocion_predominante',
                'idx_comprension','idx_atencion','idx_nivelacion','idx_coherencia','riesgo'])
    for resp, survey, course, teacher, student in rows:
        w.writerow([
            resp.fecha.strftime('%Y-%m-%d %H:%M'),
            student.nombre, course.nombre, teacher.nombre,
            resp.calidad_clase, resp.comprension_tema, resp.evaluacion_docente,
            resp.comentario or '',
            resp.sentimiento_label, resp.emocion_predominante,
            resp.indice_comprension, resp.indice_atencion,
            resp.indice_nivelacion, resp.indice_coherencia_emocional,
            resp.riesgo_insatisfaccion,
        ])
    output = si.getvalue()
    return Response(output, mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment;filename=edusatisface_datos.csv'})

# ── Admin: teachers ──────────────────────────────────────────────────
@api_bp.route('/admin/teachers')
@login_required
def admin_teachers():
    from sqlalchemy import func
    from app.models.models import Survey as S, Course as C
    teachers = db.session.query(
        Teacher,
        User,
        func.count(S.id).label('n_surveys'),
        func.count(db.session.query(C.id).filter(C.id==S.course_id).scalar_subquery()).label('n_cursos'),
    ).join(User, Teacher.user_id == User.id)\
     .outerjoin(S, S.teacher_id == Teacher.id)\
     .group_by(Teacher.id, User.id).all()
    return jsonify({'teachers': [{
        'id': t.id, 'nombre': t.nombre, 'email': u.email,
        'especialidad': t.especialidad, 'departamento': t.departamento,
        'n_surveys': n, 'n_cursos': nc or 0,
    } for t, u, n, nc in teachers]})

@api_bp.route('/admin/teachers', methods=['POST'])
@login_required
def create_teacher():
    data = request.get_json(force=True) or {}
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'El email ya existe'}), 400
    u = User(email=data['email'], role='teacher', active=True)
    u.set_password(data.get('password','changeme123'))
    db.session.add(u); db.session.flush()
    t = Teacher(
        user_id=u.id,
        codigo=f"DOC{u.id:04d}",
        nombre=data.get('nombre','Nuevo Docente'),
        especialidad=data.get('especialidad','General'),
        departamento=data.get('departamento','Sistemas'),
    )
    db.session.add(t); db.session.commit()
    return jsonify({'id': t.id, 'email': u.email})

# ── Admin: courses ───────────────────────────────────────────────────
@api_bp.route('/admin/courses')
@login_required
def admin_courses():
    from sqlalchemy import func
    rows = db.session.query(
        Course, func.count(Survey.id).label('n_surveys')
    ).outerjoin(Survey, Survey.course_id == Course.id)\
     .group_by(Course.id).order_by(Course.id.desc()).all()
    return jsonify({'courses': [{
        'id': c.id, 'codigo': c.codigo, 'nombre': c.nombre,
        'carrera': c.carrera, 'creditos': c.creditos, 'n_surveys': n or 0,
    } for c, n in rows]})

@api_bp.route('/admin/courses', methods=['POST'])
@login_required
def create_course():
    data = request.get_json(force=True) or {}
    if Course.query.filter_by(codigo=data.get('codigo')).first():
        return jsonify({'error': 'El código ya existe'}), 400
    c = Course(
        codigo=data['codigo'], nombre=data['nombre'],
        carrera=data.get('carrera','General'), creditos=int(data.get('creditos',4)),
    )
    db.session.add(c); db.session.commit()
    return jsonify({'id': c.id, 'nombre': c.nombre})

# ── Student: encuestas activas pendientes ────────────────────────────
@api_bp.route('/student/encuestas-activas')
@login_required
def student_encuestas_activas():
    rows = db.session.query(Survey, Teacher, Course)\
        .join(Teacher, Survey.teacher_id == Teacher.id)\
        .join(Course,  Survey.course_id  == Course.id)\
        .filter(Survey.activa == True)\
        .order_by(Survey.id.desc())\
        .limit(10).all()
    return jsonify({'surveys': [{
        'id': s.id, 'titulo': s.titulo, 'codigo_qr': s.codigo_qr,
        'docente': t.nombre, 'curso': c.nombre,
    } for s, t, c in rows]})
