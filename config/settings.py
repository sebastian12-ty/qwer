import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# En Render, monta un Disk en /var/data y define DB_PATH=/var/data/edusatisface.db
DB_PATH = os.environ.get('DB_PATH', os.path.join(BASE_DIR, 'edusatisface.db'))
DATABASE_URL = os.environ.get('DATABASE_URL', f"sqlite:///{DB_PATH}")
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'edusatisface-secret-2024')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/img/captures'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    EMOTION_CAPTURE_INTERVAL = 10

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
