from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Request, Project
from app import db
from app.utils.notifications import notify_new_request

user_bp = Blueprint('user', __name__)


@user_bp.route('/dashboard')
@login_required
def dashboard():
    requests = Request.query.filter_by(user_id=current_user.id).order_by(Request.created_at.desc()).all()
    return render_template('user/dashboard.html', requests=requests)


@user_bp.route('/request-project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def request_project(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        msg = request.form.get('message','').strip()
        r = Request(user_id=current_user.id, type='project', subject=project.name, message=msg)
        db.session.add(r)
        db.session.commit()
        notify_new_request(current_user.name, 'project', project.name)
        flash('Project request submitted! We will contact you soon.', 'success')
        return redirect(url_for('user.dashboard'))
    return render_template('user/request_project.html', project=project)


@user_bp.route('/submit-idea', methods=['GET', 'POST'])
@login_required
def submit_idea():
    if request.method == 'POST':
        subject = request.form.get('subject','').strip()
        msg     = request.form.get('message','').strip()
        r = Request(user_id=current_user.id, type='idea', subject=subject, message=msg)
        db.session.add(r)
        db.session.commit()
        notify_new_request(current_user.name, 'idea', subject)
        flash('Idea submitted! Our team will review it.', 'success')
        return redirect(url_for('user.dashboard'))
    return render_template('user/submit_idea.html')


@user_bp.route('/mentorship', methods=['GET', 'POST'])
@login_required
def mentorship():
    if request.method == 'POST':
        subject = request.form.get('subject','').strip()
        msg     = request.form.get('message','').strip()
        r = Request(user_id=current_user.id, type='mentorship', subject=subject, message=msg)
        db.session.add(r)
        db.session.commit()
        notify_new_request(current_user.name, 'mentorship', subject)
        flash('Mentorship request sent! We will schedule a session.', 'success')
        return redirect(url_for('user.dashboard'))
    return render_template('user/mentorship.html')
