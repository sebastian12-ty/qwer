from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config.settings import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config=Config):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'auth.login'

    from app.routes.auth import auth_bp
    from app.routes.student import student_bp
    from app.routes.teacher import teacher_bp
    from app.routes.coordinator import coordinator_bp
    from app.routes.admin import admin_bp
    from app.routes.survey import survey_bp
    from app.routes.api import api_bp
    from app.routes.bi import bi_bp

    app.register_blueprint(auth_bp,        url_prefix='/auth')
    app.register_blueprint(student_bp,     url_prefix='/student')
    app.register_blueprint(teacher_bp,     url_prefix='/teacher')
    app.register_blueprint(coordinator_bp, url_prefix='/coordinator')
    app.register_blueprint(admin_bp,       url_prefix='/admin')
    app.register_blueprint(survey_bp,      url_prefix='/survey')
    app.register_blueprint(api_bp,         url_prefix='/api/v1')
    app.register_blueprint(bi_bp,          url_prefix='/bi')

    from flask import redirect, url_for, render_template

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.route('/')
    def index():
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_for(f"{current_user.role}.dashboard"))
        return redirect(url_for('auth.login'))

    return app
