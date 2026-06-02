import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))

    # Ensure upload directory exists
    upload_folder = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.applications import applications_bp
    from app.routes.pipeline import pipeline_bp
    from app.routes.analytics import analytics_bp
    from app.routes.resumes import resumes_bp
    from app.routes.reminders import reminders_bp
    from app.routes.profile import profile_bp
    from app.routes.settings import settings_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(applications_bp, url_prefix='/applications')
    app.register_blueprint(pipeline_bp, url_prefix='/pipeline')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    app.register_blueprint(resumes_bp, url_prefix='/resumes')
    app.register_blueprint(reminders_bp, url_prefix='/reminders')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(settings_bp, url_prefix='/settings')

    # Import models for migration
    from app.models import user, application, resume, reminder, activity

    return app
