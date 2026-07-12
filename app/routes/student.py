from flask import Blueprint, render_template
from flask_login import login_required
student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
@login_required
def dashboard(): return render_template('student/dashboard.html')

@student_bp.route('/mis-encuestas')
@login_required
def mis_encuestas(): return render_template('student/mis_encuestas.html')

@student_bp.route('/historial')
@login_required
def historial(): return render_template('student/historial.html')

@student_bp.route('/perfil')
@login_required
def perfil(): return render_template('student/perfil.html')
