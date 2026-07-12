"""Seed: ejecutar solo si se usa aparte de run.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app import create_app, db
from app.models.models import User, Student, Teacher, Course, Survey

app = create_app()

def seed():
    with app.app_context():
        db.create_all()

        # Admin
        if not User.query.filter_by(email='admin@uni.edu').first():
            u = User(email='admin@uni.edu', role='admin')
            u.set_password('admin123')
            db.session.add(u)

        # Teacher
        if not User.query.filter_by(email='docente@uni.edu').first():
            u_t = User(email='docente@uni.edu', role='teacher')
            u_t.set_password('docente123')
            db.session.add(u_t)
            db.session.flush()
            t = Teacher(user_id=u_t.id, codigo='DOC001', nombre='Prof. García', especialidad='Algoritmos', departamento='Ingeniería de Sistemas')
            db.session.add(t)
            db.session.flush()

            c = Course(codigo='CS101', nombre='Algoritmos y Estructuras de Datos', carrera='Ingeniería de Sistemas', creditos=4)
            db.session.add(c)
            db.session.flush()

            s = Survey(titulo='Clase 1 - Introducción a Algoritmos', codigo_qr='DEMO01', teacher_id=t.id, course_id=c.id)
            db.session.add(s)

        # Student
        if not User.query.filter_by(email='estudiante@uni.edu').first():
            u_s = User(email='estudiante@uni.edu', role='student')
            u_s.set_password('student123')
            db.session.add(u_s)
            db.session.flush()
            st = Student(user_id=u_s.id, codigo='STU001', nombre='Juan Pérez', carrera='Ingeniería de Sistemas', semestre=3)
            db.session.add(st)

        db.session.commit()
        print("✅ Seed completado.")
        print("  admin@uni.edu / admin123")
        print("  docente@uni.edu / docente123")
        print("  estudiante@uni.edu / student123")
        print("  Encuesta demo: /survey/DEMO01")

if __name__ == '__main__':
    seed()
