from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), nullable=False)  # student, teacher, coordinator, admin
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, pw): self.password_hash = generate_password_hash(pw)
    def check_password(self, pw): return check_password_hash(self.password_hash, pw)

@login_manager.user_loader
def load_user(uid): return User.query.get(int(uid))

class Student(db.Model):
    __tablename__ = 'dim_estudiante'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    codigo = db.Column(db.String(20), unique=True)
    nombre = db.Column(db.String(100))
    carrera = db.Column(db.String(100))
    semestre = db.Column(db.Integer)

class Teacher(db.Model):
    __tablename__ = 'dim_docente'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    codigo = db.Column(db.String(20), unique=True)
    nombre = db.Column(db.String(100))
    especialidad = db.Column(db.String(100))
    departamento = db.Column(db.String(100))

class Course(db.Model):
    __tablename__ = 'dim_curso'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)
    nombre = db.Column(db.String(100))
    carrera = db.Column(db.String(100))
    creditos = db.Column(db.Integer)

class Survey(db.Model):
    __tablename__ = 'encuestas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    codigo_qr = db.Column(db.String(50), unique=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('dim_docente.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('dim_curso.id'))
    activa = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SurveyResponse(db.Model):
    __tablename__ = 'fact_satisfaccion'
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('encuestas.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('dim_estudiante.id'))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    # Encuesta
    calidad_clase = db.Column(db.Integer)          # 1-5
    comprension_tema = db.Column(db.Integer)        # 1-5
    evaluacion_docente = db.Column(db.Integer)      # 1-5
    comentario = db.Column(db.Text)

    # NLP
    sentimiento_score = db.Column(db.Float)
    sentimiento_label = db.Column(db.String(20))
    nlp_keywords = db.Column(db.JSON)

    # Emociones faciales
    emocion_feliz = db.Column(db.Float, default=0)
    emocion_neutral = db.Column(db.Float, default=0)
    emocion_triste = db.Column(db.Float, default=0)
    emocion_enojado = db.Column(db.Float, default=0)
    emocion_sorprendido = db.Column(db.Float, default=0)
    emocion_predominante = db.Column(db.String(30))

    # KPIs calculados
    indice_comprension = db.Column(db.Float)
    indice_atencion = db.Column(db.Float)
    indice_coherencia_emocional = db.Column(db.Float)
    indice_nivelacion = db.Column(db.Float)
    riesgo_insatisfaccion = db.Column(db.String(20))  # bajo, medio, alto

class EmotionCapture(db.Model):
    __tablename__ = 'emotion_captures'
    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.Integer, db.ForeignKey('fact_satisfaccion.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    feliz = db.Column(db.Float)
    neutral = db.Column(db.Float)
    triste = db.Column(db.Float)
    enojado = db.Column(db.Float)
    sorprendido = db.Column(db.Float)
    frame_path = db.Column(db.String(200))
