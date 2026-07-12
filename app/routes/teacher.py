from flask import Blueprint, render_template
from flask_login import login_required
teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/dashboard')
@login_required
def dashboard(): return render_template('teacher/dashboard.html')

@teacher_bp.route('/alumnos')
@login_required
def alumnos(): return render_template('teacher/alumnos.html')

@teacher_bp.route('/cursos')
@login_required
def cursos(): return render_template('teacher/cursos.html')

@teacher_bp.route('/clases')
@login_required
def clases(): return render_template('teacher/clases.html')

@teacher_bp.route('/nueva-encuesta')
@login_required
def nueva_encuesta(): return render_template('teacher/nueva_encuesta.html')
