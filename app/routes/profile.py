from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from werkzeug.utils import secure_filename
import os, json

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/')
@login_required
def index():
    return render_template('profile/index.html')

@profile_bp.route('/edit', methods=['POST'])
@login_required
def edit():
    current_user.name = request.form.get('name', '').strip() or current_user.name
    current_user.college = request.form.get('college', '').strip()
    grad_year = request.form.get('graduation_year', '')
    current_user.graduation_year = int(grad_year) if grad_year else None

    skills_raw = request.form.get('skills', '')
    if skills_raw:
        skills_list = [s.strip() for s in skills_raw.split(',') if s.strip()]
        current_user._skills = json.dumps(skills_list)

    # Handle profile photo
    photo = request.files.get('profile_photo')
    if photo and photo.filename:
        ext = photo.filename.rsplit('.', 1)[-1].lower()
        if ext in {'jpg', 'jpeg', 'png', 'gif', 'webp'}:
            filename = f"avatar_{current_user.id}.{ext}"
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            photo.save(os.path.join(upload_folder, filename))
            current_user.profile_photo = filename

    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile.index'))
