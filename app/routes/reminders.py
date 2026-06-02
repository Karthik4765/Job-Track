from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.reminder import Reminder
from app.models.application import Application
from datetime import datetime

reminders_bp = Blueprint('reminders', __name__)

@reminders_bp.route('/')
@login_required
def index():
    reminders = Reminder.query.filter_by(user_id=current_user.id)\
        .order_by(Reminder.reminder_date.asc()).all()
    applications = Application.query.filter_by(user_id=current_user.id).all()
    return render_template('reminders/index.html',
                           reminders=reminders,
                           applications=applications,
                           type_choices=Reminder.TYPE_CHOICES)

@reminders_bp.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title', '').strip()
    reminder_date = request.form.get('reminder_date', '')
    reminder_time = request.form.get('reminder_time', '')
    type_ = request.form.get('type', 'other')
    notes = request.form.get('notes', '').strip()
    app_id = request.form.get('application_id') or None

    if not title or not reminder_date or not reminder_time:
        flash('Title, date and time are required.', 'error')
        return redirect(url_for('reminders.index'))

    reminder = Reminder(
        user_id=current_user.id,
        application_id=int(app_id) if app_id else None,
        title=title,
        reminder_date=datetime.strptime(f"{reminder_date}T{reminder_time}", '%Y-%m-%dT%H:%M'),
        type=type_,
        notes=notes
    )
    db.session.add(reminder)
    db.session.commit()
    flash('Reminder added!', 'success')
    return redirect(url_for('reminders.index'))

@reminders_bp.route('/<int:rid>/toggle', methods=['POST'])
@login_required
def toggle(rid):
    reminder = Reminder.query.filter_by(id=rid, user_id=current_user.id).first_or_404()
    reminder.is_done = not reminder.is_done
    db.session.commit()
    return jsonify({'success': True, 'is_done': reminder.is_done})

@reminders_bp.route('/<int:rid>/delete', methods=['POST'])
@login_required
def delete(rid):
    reminder = Reminder.query.filter_by(id=rid, user_id=current_user.id).first_or_404()
    db.session.delete(reminder)
    db.session.commit()
    flash('Reminder deleted.', 'info')
    return redirect(url_for('reminders.index'))

@reminders_bp.route('/api/events')
@login_required
def api_events():
    reminders = Reminder.query.filter_by(user_id=current_user.id).all()
    events = []
    for r in reminders:
        events.append({
            'id': r.id,
            'title': r.title,
            'start': r.reminder_date.isoformat(),
            'color': r.type_color,
            'extendedProps': {
                'type': r.type,
                'notes': r.notes or '',
                'is_done': r.is_done
            }
        })
    return jsonify(events)
