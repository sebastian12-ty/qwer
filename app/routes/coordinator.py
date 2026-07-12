from flask import Blueprint, render_template
from flask_login import login_required
coordinator_bp = Blueprint('coordinator', __name__)

@coordinator_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('coordinator/dashboard.html')
