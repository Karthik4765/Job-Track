from app import db
from datetime import datetime

class Reminder(db.Model):
    __tablename__ = 'reminders'

    TYPE_CHOICES = [
        ('interview', 'Interview'),
        ('assessment', 'Assessment'),
        ('followup', 'Follow-up'),
        ('deadline', 'Deadline'),
        ('other', 'Other'),
    ]

    TYPE_COLORS = {
        'interview': '#8B5CF6',
        'assessment': '#F59E0B',
        'followup': '#3B82F6',
        'deadline': '#EF4444',
        'other': '#6B7280',
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    reminder_date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(20), default='other')
    notes = db.Column(db.Text)
    is_done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def type_label(self):
        return dict(self.TYPE_CHOICES).get(self.type, self.type)

    @property
    def type_color(self):
        return self.TYPE_COLORS.get(self.type, '#6B7280')

    def __repr__(self):
        return f'<Reminder {self.title}>'
