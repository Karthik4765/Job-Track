from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models.application import Application
from app.models.activity import Activity
from datetime import datetime

pipeline_bp = Blueprint('pipeline', __name__)

@pipeline_bp.route('/')
@login_required
def index():
    statuses = ['applied', 'assessment', 'technical_interview', 'hr_interview', 'selected', 'rejected']
    columns = {}
    for status in statuses:
        columns[status] = Application.query.filter_by(
            user_id=current_user.id, status=status
        ).order_by(Application.updated_at.desc()).all()

    return render_template('pipeline/index.html', columns=columns,
                           status_choices=Application.STATUS_CHOICES)

@pipeline_bp.route('/update-status', methods=['POST'])
@login_required
def update_status():
    data = request.get_json()
    app_id = data.get('app_id')
    new_status = data.get('status')

    application = Application.query.filter_by(id=app_id, user_id=current_user.id).first()
    if not application:
        return jsonify({'success': False, 'error': 'Not found'}), 404

    old_status = application.status
    application.status = new_status
    application.updated_at = datetime.utcnow()

    activity = Activity(
        user_id=current_user.id,
        application_id=app_id,
        action=f'{application.company_name} moved to {application.status_label}',
        icon='arrow-right'
    )
    db.session.add(activity)
    db.session.commit()

    return jsonify({'success': True, 'status': new_status, 'label': application.status_label})
