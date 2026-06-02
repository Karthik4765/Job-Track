from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.application import Application
from app.models.activity import Activity
from app.models.reminder import Reminder
from datetime import datetime, timedelta
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    apps = Application.query.filter_by(user_id=current_user.id)

    stats = {
        'total': apps.count(),
        'applied': apps.filter_by(status='applied').count(),
        'assessment': apps.filter_by(status='assessment').count(),
        'technical_interview': apps.filter_by(status='technical_interview').count(),
        'hr_interview': apps.filter_by(status='hr_interview').count(),
        'selected': apps.filter_by(status='selected').count(),
        'rejected': apps.filter_by(status='rejected').count(),
    }
    stats['interview'] = stats['technical_interview'] + stats['hr_interview']

    recent_activities = Activity.query.filter_by(user_id=current_user.id)\
        .order_by(Activity.created_at.desc()).limit(8).all()

    upcoming = Reminder.query.filter_by(user_id=current_user.id, is_done=False)\
        .filter(Reminder.reminder_date >= datetime.utcnow())\
        .filter(Reminder.reminder_date <= datetime.utcnow() + timedelta(days=14))\
        .order_by(Reminder.reminder_date.asc()).limit(5).all()

    recent_apps = Application.query.filter_by(user_id=current_user.id)\
        .order_by(Application.created_at.desc()).limit(5).all()

    return render_template('dashboard/index.html',
                           stats=stats,
                           recent_activities=recent_activities,
                           upcoming=upcoming,
                           recent_apps=recent_apps,
                           now=datetime.utcnow())
