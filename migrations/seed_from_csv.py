"""
Carga los 5,200 registros del CSV en la BD SQLite.
Ejecutar una sola vez: python migrations/seed_from_csv.py
"""
import os, sys, csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app, db
from app.models.models import (
    User, Student, Teacher, Course, Survey, SurveyResponse, EmotionCapture
)
from datetime import datetime

app  = create_app()
DATA = os.path.join(os.path.dirname(__file__), '..', 'data_exports')

EMOCIONES = ['feliz','neutral','triste','enojado','sorprendido']

def run():
    with app.app_context():
        db.create_all()

        # --- Skip if already seeded ---
        if SurveyResponse.query.count() > 100:
            print(f"✅ Ya hay {SurveyResponse.query.count()} respuestas. Sin cambios.")
            return

        print("Cargando datos desde CSVs...")

        # 1. Usuarios base (si no existen)
        if not User.query.filter_by(email='admin@uni.edu').first():
            for email, role, pw in [
                ('admin@uni.edu','admin','admin123'),
                ('docente@uni.edu','teacher','docente123'),
                ('estudiante@uni.edu','student','student123'),
            ]:
                u = User(email=email, role=role, active=True)
                u.set_password(pw)
                db.session.add(u)
            db.session.flush()

        # 2. Docentes
        teacher_ids = {}
        with open(f'{DATA}/paso1_fuentes_estudiantes.csv', encoding='utf-8') as f:
            pass  # estudiantes los creamos desde fact

        # Crear docentes base
        doc_emails = {}
        for i in range(1, 11):
            email = f'docente{i}@uni.edu'
            u = User.query.filter_by(email=email).first()
            if not u:
                u = User(email=email, role='teacher', active=True)
                u.set_password('docente123')
                db.session.add(u)
                db.session.flush()
            doc_emails[i] = u.id

        doc_names = {
            1:'Dr. Carlos García',2:'Mg. Ana Rodríguez',3:'Dr. Luis Mendoza',
            4:'Mg. María Torres',5:'Dr. Jorge Quispe',6:'Mg. Rosa Huamán',
            7:'Dr. Pedro Vargas',8:'Mg. Elena Castillo',9:'Dr. Roberto Silva',10:'Mg. Carmen Flores',
        }
        teacher_db_ids = {}
        for tid, name in doc_names.items():
            t = Teacher.query.filter_by(codigo=f'DOC{tid:03d}').first()
            if not t:
                t = Teacher(user_id=doc_emails[tid], codigo=f'DOC{tid:03d}',
                            nombre=name, especialidad='General', departamento='Ingeniería')
                db.session.add(t); db.session.flush()
            teacher_db_ids[tid] = t.id

        # 3. Cursos únicos desde fact CSV
        curso_ids = {}
        with open(f'{DATA}/paso4_fact_satisfaccion.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                nombre = row['curso']
                carrera = row['carrera']
                key = f"{carrera}::{nombre}"
                if key not in curso_ids:
                    c = Course.query.filter_by(nombre=nombre, carrera=carrera).first()
                    if not c:
                        c = Course(codigo=f'C{len(curso_ids)+1:04d}', nombre=nombre,
                                   carrera=carrera, creditos=4)
                        db.session.add(c); db.session.flush()
                    curso_ids[key] = c.id
        print(f"  ✅ {len(curso_ids)} cursos")

        # 4. Encuestas únicas
        survey_ids = {}
        with open(f'{DATA}/paso4_fact_satisfaccion.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sid = int(row['survey_id'])
                if sid not in survey_ids:
                    key = f"{row['carrera']}::{row['curso']}"
                    tid_orig = int(row['teacher_id'])
                    t_db_id  = teacher_db_ids.get(tid_orig, teacher_db_ids[1])
                    c_db_id  = curso_ids.get(key, list(curso_ids.values())[0])
                    s = Survey.query.filter_by(codigo_qr=f'QR{sid:04d}').first()
                    if not s:
                        s = Survey(
                            titulo=f"{row['curso']} — Clase {sid}",
                            codigo_qr=f'QR{sid:04d}',
                            teacher_id=t_db_id, course_id=c_db_id, activa=True,
                        )
                        db.session.add(s); db.session.flush()
                    survey_ids[sid] = s.id
        print(f"  ✅ {len(survey_ids)} encuestas")

        # 5. Estudiantes
        student_ids = {}
        with open(f'{DATA}/paso1_fuentes_estudiantes.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                orig_id = int(row['id'])
                email = f"stu{orig_id}@uni.edu"
                u = User.query.filter_by(email=email).first()
                if not u:
                    u = User(email=email, role='student', active=True)
                    u.set_password('student123')
                    db.session.add(u); db.session.flush()
                st = Student.query.filter_by(codigo=row['codigo']).first()
                if not st:
                    st = Student(user_id=u.id, codigo=row['codigo'],
                                 nombre=row['nombre'], carrera=row['carrera'],
                                 semestre=int(row['semestre']))
                    db.session.add(st); db.session.flush()
                student_ids[orig_id] = st.id
        print(f"  ✅ {len(student_ids)} estudiantes")

        # 6. Respuestas (fact_satisfaccion) — en lotes
        BATCH = 200
        batch_resp = []
        total = 0
        with open(f'{DATA}/paso4_fact_satisfaccion.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                orig_student = int(row['student_id'])
                orig_survey  = int(row['survey_id'])
                st_id = student_ids.get(orig_student)
                sv_id = survey_ids.get(orig_survey)
                if not st_id or not sv_id: continue
                try:
                    fecha = datetime.strptime(row['fecha'], '%Y-%m-%d %H:%M:%S')
                except:
                    fecha = datetime.utcnow()
                resp = SurveyResponse(
                    survey_id=sv_id, student_id=st_id, fecha=fecha,
                    calidad_clase=int(float(row.get('calidad_clase',3))),
                    comprension_tema=int(float(row.get('comprension_tema',3))),
                    evaluacion_docente=int(float(row.get('evaluacion_docente',3))),
                    comentario=row.get('comentario',''),
                    sentimiento_score=float(row.get('sentimiento_score',0.5) or 0.5),
                    sentimiento_label=row.get('sentimiento_label','neutral'),
                    nlp_keywords=[],
                    emocion_feliz=float(row.get('emocion_feliz',0) or 0),
                    emocion_neutral=float(row.get('emocion_neutral',0) or 0),
                    emocion_triste=float(row.get('emocion_triste',0) or 0),
                    emocion_enojado=float(row.get('emocion_enojado',0) or 0),
                    emocion_sorprendido=float(row.get('emocion_sorprendido',0) or 0),
                    emocion_predominante=row.get('emocion_predominante','neutral'),
                    indice_comprension=float(row.get('indice_comprension',0.5) or 0.5),
                    indice_atencion=float(row.get('indice_atencion',0.5) or 0.5),
                    indice_coherencia_emocional=float(row.get('indice_coherencia_emocional',0.5) or 0.5),
                    indice_nivelacion=float(row.get('indice_nivelacion',0.5) or 0.5),
                    riesgo_insatisfaccion=row.get('riesgo_insatisfaccion','medio'),
                )
                batch_resp.append(resp)
                if len(batch_resp) >= BATCH:
                    db.session.bulk_save_objects(batch_resp)
                    db.session.commit()
                    total += len(batch_resp)
                    batch_resp = []
                    print(f"  ... {total} filas insertadas", end='\r')
        if batch_resp:
            db.session.bulk_save_objects(batch_resp)
            db.session.commit()
            total += len(batch_resp)

        print(f"\n  ✅ {total} respuestas insertadas en SQLite")
        print(f"\n{'='*50}")
        print(f"  SEED COMPLETO")
        print(f"  BD tiene {SurveyResponse.query.count():,} respuestas")
        print(f"  BD tiene {Student.query.count():,} estudiantes")
        print(f"  BD tiene {Survey.query.count():,} encuestas")
        print(f"{'='*50}")

if __name__ == '__main__':
    run()
