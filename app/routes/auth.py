import random, string
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, OTPVerification
from app import db
from app.utils.notifications import send_otp_email, notify_new_user

auth_bp = Blueprint('auth', __name__)


def _gen_otp():
    return ''.join(random.choices(string.digits, k=6))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    if request.method == 'POST':
        name  = request.form.get('name','').strip()
        email = request.form.get('email','').strip().lower()
        pw    = request.form.get('password','')
        pw2   = request.form.get('confirm_password','')
        if pw != pw2:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('auth.login'))
        # Save pending user in session
        session['pending_name']  = name
        session['pending_email'] = email
        session['pending_pw']    = pw
        # Generate & send OTP
        otp = _gen_otp()
        OTPVerification.query.filter_by(email=email).delete()
        db.session.add(OTPVerification(email=email, otp=otp, expiry=datetime.utcnow()+timedelta(minutes=10)))
        db.session.commit()
        send_otp_email(email, otp)
        flash(f'OTP sent to {email}. Check your inbox.', 'info')
        return redirect(url_for('auth.verify_otp'))
    return render_template('auth/register.html')


@auth_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered = request.form.get('otp','').strip()
        email   = session.get('pending_email')
        if not email:
            flash('Session expired. Register again.', 'danger')
            return redirect(url_for('auth.register'))
        record = OTPVerification.query.filter_by(email=email, otp=entered).first()
        if not record or record.expiry < datetime.utcnow():
            flash('Invalid or expired OTP.', 'danger')
            return render_template('auth/verify_otp.html')
        # Create user
        user = User(name=session['pending_name'], email=email, is_verified=True)
        user.set_password(session['pending_pw'])
        db.session.add(user)
        OTPVerification.query.filter_by(email=email).delete()
        db.session.commit()
        session.pop('pending_name', None)
        session.pop('pending_email', None)
        session.pop('pending_pw', None)
        notify_new_user(user.name, user.email)
        login_user(user)
        flash('Account created successfully! Welcome to NewStar Infosis.', 'success')
        return redirect(url_for('user.dashboard'))
    return render_template('auth/verify_otp.html')


@auth_bp.route('/resend-otp')
def resend_otp():
    email = session.get('pending_email')
    if not email:
        return redirect(url_for('auth.register'))
    otp = _gen_otp()
    OTPVerification.query.filter_by(email=email).delete()
    db.session.add(OTPVerification(email=email, otp=otp, expiry=datetime.utcnow()+timedelta(minutes=10)))
    db.session.commit()
    send_otp_email(email, otp)
    flash('New OTP sent!', 'info')
    return redirect(url_for('auth.verify_otp'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard') if not current_user.is_admin else url_for('admin.dashboard'))
    if request.method == 'POST':
        email = request.form.get('email','').strip().lower()
        pw    = request.form.get('password','')
        user  = User.query.filter_by(email=email).first()
        if not user or not user.check_password(pw):
            flash('Invalid email or password.', 'danger')
            return render_template('auth/login.html')
        if not user.is_verified:
            flash('Please verify your email first.', 'warning')
            return render_template('auth/login.html')
        login_user(user, remember=True)
        flash(f'Welcome back, {user.name}!', 'success')
        if user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('public.index'))
