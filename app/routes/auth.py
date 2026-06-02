from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from datetime import datetime, timedelta
from email.message import EmailMessage
import random
import smtplib

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        college = request.form.get('college', '').strip()
        graduation_year = request.form.get('graduation_year', '')

        if not all([name, email, password, confirm_password]):
            flash('All fields are required.', 'error')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('auth/register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please log in.', 'error')
            return render_template('auth/register.html')

        user = User(
            name=name,
            email=email,
            college=college,
            graduation_year=int(graduation_year) if graduation_year else None
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f'Welcome to JobTrack, {name}!', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False) == 'on'

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user = User.query.filter_by(email=email).first()

        if user:
            otp = '{:06d}'.format(random.randrange(100000, 1000000))
            session['password_reset'] = {
                'email': email,
                'otp': otp,
                'expires_at': (datetime.utcnow() + timedelta(minutes=10)).isoformat()
            }
            try:
                send_reset_email(email, otp)
                flash('A 6-digit OTP has been sent to your email if it exists.', 'info')
                return redirect(url_for('auth.reset_password'))
            except Exception as e:
                current_app.logger.error(f'Failed to send reset OTP: {e}')
                flash('Unable to send reset email right now. Please try again later.', 'error')
                session.pop('password_reset', None)
                return render_template('auth/forgot_password.html')

        flash('A 6-digit OTP has been sent to your email if it exists.', 'info')
    return render_template('auth/forgot_password.html')


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    saved = session.get('password_reset')
    if not saved:
        flash('Please request a password reset OTP first.', 'info')
        return redirect(url_for('auth.forgot_password'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        otp = request.form.get('otp', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not all([email, otp, password, confirm_password]):
            flash('All fields are required.', 'error')
            return render_template('auth/reset_password.html', email=email)

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/reset_password.html', email=email)

        if not saved or saved.get('email') != email or saved.get('otp') != otp:
            flash('Invalid OTP or email. Please request a new one.', 'error')
            return redirect(url_for('auth.forgot_password'))

        expires_at = datetime.fromisoformat(saved.get('expires_at'))
        if datetime.utcnow() > expires_at:
            session.pop('password_reset', None)
            flash('OTP expired. Please request a new one.', 'error')
            return redirect(url_for('auth.forgot_password'))

        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Invalid email. Please try again.', 'error')
            return redirect(url_for('auth.forgot_password'))

        user.set_password(password)
        db.session.commit()
        session.pop('password_reset', None)
        flash('Your password has been reset. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', email=(saved.get('email') if saved else ''))


@auth_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    saved = session.get('password_reset')
    if not saved:
        flash('Please request a new OTP from the forgot password page.', 'error')
        return redirect(url_for('auth.forgot_password'))

    email = request.form.get('email', '').strip().lower()
    if email and email != saved.get('email'):
        flash('Email does not match the current reset session.', 'error')
        return redirect(url_for('auth.reset_password'))

    otp = '{:06d}'.format(random.randrange(100000, 1000000))
    saved['otp'] = otp
    saved['expires_at'] = (datetime.utcnow() + timedelta(minutes=10)).isoformat()
    session['password_reset'] = saved

    try:
        send_reset_email(saved.get('email'), otp)
        flash('A new OTP has been sent to your email.', 'success')
    except Exception as e:
        current_app.logger.error(f'Failed to resend reset OTP: {e}')
        flash('Unable to send the OTP right now. Please try again later.', 'error')
    return redirect(url_for('auth.reset_password'))


def send_reset_email(to_email, otp):
    msg = EmailMessage()
    sender = current_app.config.get('MAIL_DEFAULT_SENDER')
    msg['Subject'] = 'JobTrack Password Reset OTP'
    msg['From'] = sender
    msg['To'] = to_email
    msg.set_content(f"Your JobTrack password reset OTP is: {otp}\n\nThis code will expire in 10 minutes. If you did not request a reset, please ignore this email.")

    smtp_server = current_app.config.get('MAIL_SERVER')
    smtp_port = current_app.config.get('MAIL_PORT')
    smtp_username = current_app.config.get('MAIL_USERNAME')
    smtp_password = current_app.config.get('MAIL_PASSWORD')
    use_tls = current_app.config.get('MAIL_USE_TLS', True)

    if not smtp_username or not smtp_password:
        raise RuntimeError('SMTP credentials are not configured.')

    with smtplib.SMTP(smtp_server, smtp_port, timeout=20) as server:
        if use_tls:
            server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
