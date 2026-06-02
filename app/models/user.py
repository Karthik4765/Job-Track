from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    college = db.Column(db.String(200))
    graduation_year = db.Column(db.Integer)
    _skills = db.Column('skills', db.Text)
    profile_photo = db.Column(db.String(255))
    theme = db.Column(db.String(10), default='dark')
    notifications_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    resumes = db.relationship('Resume', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    reminders = db.relationship('Reminder', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    activities = db.relationship('Activity', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def skills(self):
        if self._skills:
            try:
                return json.loads(self._skills)
            except:
                return []
        return []

    @skills.setter
    def skills(self, value):
        if isinstance(value, list):
            self._skills = json.dumps(value)
        elif isinstance(value, str):
            self._skills = value

    def __repr__(self):
        return f'<User {self.email}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
