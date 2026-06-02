from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models.application import Application
from sqlalchemy import func, extract
from app import db
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/')
@login_required
def index():
    apps = Application.query.filter_by(user_id=current_user.id)
    total = apps.count()

    status_data = {}
    for status, label in Application.STATUS_CHOICES:
        status_data[label] = apps.filter_by(status=status).count()

    selected = apps.filter_by(status='selected').count()
    rejected = apps.filter_by(status='rejected').count()
    interviews = apps.filter(Application.status.in_(
        ['technical_interview', 'hr_interview', 'selected'])).count()

    success_rate = round((selected / total * 100), 1) if total > 0 else 0
    interview_rate = round((interviews / total * 100), 1) if total > 0 else 0
    selection_rate = round((selected / interviews * 100), 1) if interviews > 0 else 0

    # Monthly data for last 6 months
    monthly_data = []
    for i in range(5, -1, -1):
        date = datetime.utcnow() - timedelta(days=30 * i)
        count = apps.filter(
            extract('month', Application.application_date) == date.month,
            extract('year', Application.application_date) == date.year
        ).count()
        monthly_data.append({'month': date.strftime('%b %Y'), 'count': count})

    # Company stats
    company_stats = db.session.query(
        Application.company_name,
        func.count(Application.id).label('count'),
        Application.status
    ).filter_by(user_id=current_user.id)\
     .group_by(Application.company_name, Application.status)\
     .order_by(func.count(Application.id).desc()).limit(10).all()

    company_map = {}
    for row in company_stats:
        if row.company_name not in company_map:
            company_map[row.company_name] = {'total': 0, 'selected': 0, 'rejected': 0}
        company_map[row.company_name]['total'] += row.count
        if row.status == 'selected':
            company_map[row.company_name]['selected'] += row.count
        elif row.status == 'rejected':
            company_map[row.company_name]['rejected'] += row.count

    return render_template('analytics/index.html',
                           total=total,
                           status_data=status_data,
                           success_rate=success_rate,
                           interview_rate=interview_rate,
                           selection_rate=selection_rate,
                           monthly_data=monthly_data,
                           company_map=company_map,
                           selected=selected,
                           rejected=rejected,
                           interviews=interviews)
