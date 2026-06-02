import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # Database Configuration
    database_url = os.environ.get('DATABASE_URL')

    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///jobtrack.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File Upload Configuration
    MAX_CONTENT_LENGTH = int(
        os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)
    )

    UPLOAD_FOLDER = os.environ.get(
        'UPLOAD_FOLDER',
        'app/static/uploads'
    )

    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

    # Email Configuration
    MAIL_SERVER = os.environ.get(
        'MAIL_SERVER',
        'smtp.gmail.com'
    )

    MAIL_PORT = int(
        os.environ.get('MAIL_PORT', 587)
    )

    MAIL_USE_TLS = os.environ.get(
        'MAIL_USE_TLS',
        'true'
    ).lower() in ['true', '1', 'yes']

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')

    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    MAIL_DEFAULT_SENDER = os.environ.get(
        'MAIL_DEFAULT_SENDER',
        MAIL_USERNAME
    )


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}