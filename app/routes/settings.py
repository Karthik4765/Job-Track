from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/')
@login_required
def index():
    return render_template('settings/index.html')

@settings_bp.route('/theme', methods=['POST'])
@login_required
def set_theme():
    theme = request.form.get('theme', 'dark')
    if theme in ('dark', 'light'):
        current_user.theme = theme
        db.session.commit()
    return redirect(url_for('settings.index'))

@settings_bp.route('/notifications', methods=['POST'])
@login_required
def set_notifications():
    current_user.notifications_enabled = request.form.get('notifications') == 'on'
    db.session.commit()
    flash('Notification preferences saved.', 'success')
    return redirect(url_for('settings.index'))

@settings_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    if not current_user.check_password(current_password):
        flash('Current password is incorrect.', 'error')
        return redirect(url_for('settings.index'))

    if new_password != confirm_password:
        flash('New passwords do not match.', 'error')
        return redirect(url_for('settings.index'))

    if len(new_password) < 6:
        flash('Password must be at least 6 characters.', 'error')
        return redirect(url_for('settings.index'))

    current_user.set_password(new_password)
    db.session.commit()
    flash('Password changed successfully!', 'success')
    return redirect(url_for('settings.index'))
