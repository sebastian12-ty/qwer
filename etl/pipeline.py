"""
ETL Pipeline: Extrae, transforma y carga datos al Data Warehouse.
Ejecutar: python etl/pipeline.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app, db
from app.models.models import SurveyResponse
from sqlalchemy import text
from datetime import datetime

app = create_app()

def extract():
    with app.app_context():
        rows = db.session.execute(text("""
            SELECT fs.*, u.email, de.nombre as estudiante, dd.nombre as docente,
                   dc.nombre as curso, dc.carrera
            FROM fact_satisfaccion fs
            JOIN dim_estudiante de ON de.id = fs.student_id
            JOIN users u ON u.id = de.user_id
            JOIN encuestas e ON e.id = fs.survey_id
            JOIN dim_docente dd ON dd.id = e.teacher_id
            JOIN dim_curso dc ON dc.id = e.course_id
        """)).fetchall()
        print(f"[ETL] Extraídas {len(rows)} filas")
        return rows

def transform(rows):
    transformed = []
    for r in rows:
        rec = dict(r._mapping)
        # Calcular dimensión tiempo
        fecha = rec.get('fecha', datetime.utcnow())
        rec['anio'] = fecha.year
        rec['mes'] = fecha.month
        rec['semana'] = fecha.isocalendar()[1]
        rec['dia_semana'] = fecha.weekday()
        # Normalizar scores a porcentaje
        for k in ['indice_comprension', 'indice_atencion', 'indice_coherencia_emocional', 'indice_nivelacion']:
            if rec.get(k) is not None:
                rec[f'{k}_pct'] = round(rec[k] * 100, 1)
        transformed.append(rec)
    print(f"[ETL] Transformadas {len(transformed)} filas")
    return transformed

def load(records):
    # En producción: insertar en tablas DW separadas (star schema)
    print(f"[ETL] Cargando {len(records)} registros al DW...")
    for rec in records:
        print(f"  - Estudiante: {rec.get('estudiante')} | Curso: {rec.get('curso')} | Nivelación: {rec.get('indice_nivelacion_pct')}%")
    print("[ETL] Carga completada.")

def run():
    rows = extract()
    transformed = transform(rows)
    load(transformed)

if __name__ == '__main__':
    run()
