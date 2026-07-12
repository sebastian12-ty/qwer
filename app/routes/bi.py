from flask import Blueprint, render_template, send_file, abort, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.utils.decorators import admin_required
from werkzeug.utils import secure_filename
import os, csv, json, time

bi_bp = Blueprint('bi', __name__)

CSV_MAP = {
    1: 'paso1_fuentes_estudiantes.csv',
    2: 'paso2_iot_capturas.csv',
    3: 'paso3_etl_respuestas.csv',
    4: 'paso4_fact_satisfaccion.csv',
    5: 'paso5_ia_resultados.csv',
    6: 'paso6_kpis_semanticos.csv',
    7: 'paso7_looker_dataset_maestro.csv',
}

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'data_exports'
)
UPLOADS_DIR = os.path.join(DATA_DIR, 'uploads')
os.makedirs(UPLOADS_DIR, exist_ok=True)

def _ensure_data():
    master = os.path.join(DATA_DIR, 'paso7_looker_dataset_maestro.csv')
    if not os.path.exists(master):
        import subprocess, sys
        gen = os.path.join(DATA_DIR, 'generate_data.py')
        subprocess.run([sys.executable, gen], check=True, timeout=120)

# ── Todas las rutas BI son SOLO ADMIN ───────────────────────────────
@bi_bp.route('/pipeline')
@login_required
@admin_required
def pipeline():
    return render_template('bi/pipeline.html')

@bi_bp.route('/datos')
@login_required
@admin_required
def datos():
    uploaded = []
    if os.path.exists(UPLOADS_DIR):
        for fname in sorted(os.listdir(UPLOADS_DIR), reverse=True):
            if fname.endswith('.csv'):
                path = os.path.join(UPLOADS_DIR, fname)
                try:
                    with open(path, encoding='utf-8') as f:
                        rows = sum(1 for _ in f) - 1
                except Exception:
                    rows = '?'
                uploaded.append({
                    'name': fname,
                    'rows': rows,
                    'size_kb': round(os.path.getsize(path)/1024, 1),
                    'mtime': time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(path))),
                })
    return render_template('bi/datos.html', uploaded=uploaded)

@bi_bp.route('/download/<int:step>')
@login_required
@admin_required
def download(step):
    filename = CSV_MAP.get(step)
    if not filename:
        abort(404)
    _ensure_data()
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        abort(500)
    return send_file(filepath, as_attachment=True, download_name=filename, mimetype='text/csv')

@bi_bp.route('/resumen')
@login_required
@admin_required
def resumen():
    _ensure_data()
    path = os.path.join(DATA_DIR, 'resumen_ejecutivo.csv')
    if not os.path.exists(path):
        return jsonify({})
    with open(path, encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    return jsonify(rows[0] if rows else {})

@bi_bp.route('/stats')
@login_required
@admin_required
def stats():
    _ensure_data()
    result = {}
    for step, fname in CSV_MAP.items():
        path = os.path.join(DATA_DIR, fname)
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                result[f'paso{step}'] = sum(1 for _ in f) - 1
        else:
            result[f'paso{step}'] = 0
    return jsonify(result)

# ── Subida de CSV propio ────────────────────────────────────────────
ALLOWED_EXT = {'csv'}

def _allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@bi_bp.route('/upload', methods=['POST'])
@login_required
@admin_required
def upload_csv():
    if 'file' not in request.files:
        flash('No se seleccionó ningún archivo.', 'danger')
        return redirect(url_for('bi.datos'))
    file = request.files['file']
    if file.filename == '' or not _allowed(file.filename):
        flash('Selecciona un archivo .csv válido.', 'danger')
        return redirect(url_for('bi.datos'))

    filename = secure_filename(file.filename)
    ts = time.strftime('%Y%m%d_%H%M%S')
    final_name = f"{ts}_{filename}"
    filepath = os.path.join(UPLOADS_DIR, final_name)
    file.save(filepath)

    # Validar que sea CSV legible
    try:
        with open(filepath, encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = sum(1 for _ in reader)
        flash(f'✅ Archivo "{filename}" subido correctamente — {rows} filas, {len(header)} columnas.', 'success')
    except Exception as e:
        os.remove(filepath)
        flash(f'Error al leer el CSV: {e}', 'danger')

    return redirect(url_for('bi.datos'))

@bi_bp.route('/upload/<filename>/delete', methods=['POST'])
@login_required
@admin_required
def delete_upload(filename):
    filepath = os.path.join(UPLOADS_DIR, secure_filename(filename))
    if os.path.exists(filepath):
        os.remove(filepath)
        flash('Archivo eliminado.', 'success')
    return redirect(url_for('bi.datos'))

@bi_bp.route('/upload/<filename>/download')
@login_required
@admin_required
def download_upload(filename):
    filepath = os.path.join(UPLOADS_DIR, secure_filename(filename))
    if not os.path.exists(filepath):
        abort(404)
    return send_file(filepath, as_attachment=True, download_name=filename, mimetype='text/csv')

@bi_bp.route('/upload/<filename>/preview')
@login_required
@admin_required
def preview_upload(filename):
    filepath = os.path.join(UPLOADS_DIR, secure_filename(filename))
    if not os.path.exists(filepath):
        abort(404)
    with open(filepath, encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for _, row in zip(range(20), reader)]
    return jsonify({'header': header, 'rows': rows})

# ── Diagrama de estrella: metadata en vivo ──────────────────────────
@bi_bp.route('/star-schema')
@login_required
@admin_required
def star_schema():
    """Retorna metadata del modelo estrella + conteo de filas en vivo desde la BD real."""
    from app import db
    from app.models.models import SurveyResponse, Student, Teacher, Course, Survey
    return jsonify({
        'fact': {
            'name': 'Fact_Satisfaccion',
            'rows': SurveyResponse.query.count(),
            'fields': ['calidad_clase','comprension_tema','evaluacion_docente',
                       'sentimiento_score','indice_comprension','indice_atencion',
                       'indice_coherencia_emocional','indice_nivelacion','riesgo_insatisfaccion'],
        },
        'dimensions': [
            {'name': 'Dim_Estudiante', 'rows': Student.query.count(), 'fields': ['codigo','nombre','carrera','semestre']},
            {'name': 'Dim_Docente',    'rows': Teacher.query.count(), 'fields': ['codigo','nombre','especialidad','departamento']},
            {'name': 'Dim_Curso',      'rows': Course.query.count(),  'fields': ['codigo','nombre','carrera','creditos']},
            {'name': 'Dim_Encuesta',   'rows': Survey.query.count(),  'fields': ['titulo','codigo_qr','activa']},
            {'name': 'Dim_Tiempo',     'rows': SurveyResponse.query.count(), 'fields': ['fecha','anio','mes','dia_semana']},
        ],
        'last_updated': __import__('datetime').datetime.utcnow().isoformat(),
    })

@bi_bp.route('/star-schema-view')
@login_required
@admin_required
def star_schema_view():
    return render_template('bi/star_schema.html')
