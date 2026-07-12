import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.models import User, Student, Teacher, Course, Survey

app = create_app()

def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='admin@uni.edu').first():
            _seed_base()
            print("✅ Base de datos creada con datos base.")
        else:
            print(f"✅ BD lista — {__import__('app.models.models', fromlist=['SurveyResponse']).SurveyResponse.query.count()} respuestas.")

def _seed_base():
    # Admin
    u = User(email='admin@uni.edu', role='admin', active=True)
    u.set_password('admin123')
    db.session.add(u)

    # Teacher
    u_t = User(email='docente@uni.edu', role='teacher', active=True)
    u_t.set_password('docente123')
    db.session.add(u_t); db.session.flush()
    t = Teacher(user_id=u_t.id, codigo='DOC001', nombre='Prof. García',
                especialidad='Algoritmos', departamento='Ingeniería de Sistemas')
    db.session.add(t); db.session.flush()

    c = Course(codigo='CS101', nombre='Algoritmos y Estructuras de Datos',
               carrera='Ingeniería de Sistemas', creditos=4)
    db.session.add(c); db.session.flush()

    s = Survey(titulo='Clase 1 - Introducción a Algoritmos',
               codigo_qr='DEMO01', teacher_id=t.id, course_id=c.id)
    db.session.add(s)

    # Student
    u_s = User(email='estudiante@uni.edu', role='student', active=True)
    u_s.set_password('student123')
    db.session.add(u_s); db.session.flush()
    st = Student(user_id=u_s.id, codigo='STU001', nombre='Juan Pérez',
                 carrera='Ingeniería de Sistemas', semestre=3)
    db.session.add(st)
    db.session.commit()

if __name__ == '__main__':
    init_db()
    print("\n🚀 Servidor en http://localhost:5000")
    print("   Encuesta demo  → http://localhost:5000/survey/DEMO01")
    print("   Pipeline E2E   → http://localhost:5000/bi/pipeline")
    print("   Centro datos   → http://localhost:5000/bi/datos")
    print()
    print("   💡 Para cargar 5,200 registros en la BD:")
    print("      python migrations/seed_from_csv.py")
    print()
    app.run(debug=True, host='0.0.0.0', port=5000)
