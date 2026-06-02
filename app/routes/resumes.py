from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory, current_app
from flask_login import login_required, current_user
from app import db
from app.models.resume import Resume
from werkzeug.utils import secure_filename
import os
from datetime import datetime

resumes_bp = Blueprint('resumes', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resumes_bp.route('/')
@login_required
def index():
    resumes = Resume.query.filter_by(user_id=current_user.id)\
        .order_by(Resume.uploaded_at.desc()).all()
    return render_template('resumes/index.html', resumes=resumes)

@resumes_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    label = request.form.get('label', '').strip()
    file = request.files.get('file')

    if not label:
        flash('Please provide a label for the resume.', 'error')
        return redirect(url_for('resumes.index'))

    if not file or file.filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('resumes.index'))

    if not allowed_file(file.filename):
        flash('Only PDF, DOC, and DOCX files are allowed.', 'error')
        return redirect(url_for('resumes.index'))

    filename = secure_filename(file.filename)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    unique_filename = f"{current_user.id}_{timestamp}_{filename}"

    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, unique_filename)
    file.save(filepath)

    resume = Resume(
        user_id=current_user.id,
        label=label,
        filename=unique_filename,
        filepath=filepath
    )
    db.session.add(resume)
    db.session.commit()

    flash(f'Resume "{label}" uploaded successfully!', 'success')
    return redirect(url_for('resumes.index'))

@resumes_bp.route('/<int:resume_id>/download')
@login_required
def download(resume_id):
    resume = Resume.query.filter_by(id=resume_id, user_id=current_user.id).first_or_404()
    upload_folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(os.path.abspath(upload_folder),
                               resume.filename,
                               as_attachment=True,
                               download_name=f"{resume.label}.{resume.filename.rsplit('.', 1)[-1]}")

@resumes_bp.route('/<int:resume_id>/delete', methods=['POST'])
@login_required
def delete(resume_id):
    resume = Resume.query.filter_by(id=resume_id, user_id=current_user.id).first_or_404()
    try:
        if os.path.exists(resume.filepath):
            os.remove(resume.filepath)
    except:
        pass
    db.session.delete(resume)
    db.session.commit()
    flash(f'Resume "{resume.label}" deleted.', 'info')
    return redirect(url_for('resumes.index'))
