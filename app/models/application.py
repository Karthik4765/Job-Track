from app import db
from datetime import datetime

class Application(db.Model):
    __tablename__ = 'applications'

    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('assessment', 'Online Assessment'),
        ('technical_interview', 'Technical Interview'),
        ('hr_interview', 'HR Interview'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    STATUS_COLORS = {
        'applied': '#3B82F6',
        'assessment': '#F59E0B',
        'technical_interview': '#8B5CF6',
        'hr_interview': '#EC4899',
        'selected': '#10B981',
        'rejected': '#EF4444',
        'withdrawn': '#6B7280',
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    role_name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    package = db.Column(db.String(100))
    application_date = db.Column(db.Date)
    deadline = db.Column(db.Date)
    job_url = db.Column(db.String(500))
    status = db.Column(db.String(30), default='applied')
    notes = db.Column(db.Text)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    activities = db.relationship('Activity', backref='application', lazy='dynamic', cascade='all, delete-orphan')
    reminders = db.relationship('Reminder', backref='application', lazy='dynamic', cascade='all, delete-orphan')
    resume = db.relationship('Resume', backref='applications', foreign_keys=[resume_id])

    @property
    def status_label(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

    @property
    def status_color(self):
        return self.STATUS_COLORS.get(self.status, '#6B7280')

    def __repr__(self):
        return f'<Application {self.company_name} - {self.role_name}>'
