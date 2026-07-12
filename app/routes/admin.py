from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard(): return render_template('admin/dashboard.html')

@admin_bp.route('/usuarios')
@login_required
@admin_required
def usuarios(): return render_template('admin/usuarios.html')

@admin_bp.route('/docentes')
@login_required
@admin_required
def docentes(): return render_template('admin/docentes.html')

@admin_bp.route('/cursos')
@login_required
@admin_required
def cursos(): return render_template('admin/cursos.html')
