from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Project, TeamMember, ContactMessage, InternshipApplication
from app import db
from app.utils.notifications import notify_contact, notify_new_internship

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def index():
    projects = Project.query.order_by(Project.created_at.desc()).limit(6).all()
    team     = TeamMember.query.order_by(TeamMember.order_index).all()
    return render_template('public/index.html', projects=projects, team=team)


@public_bp.route('/projects')
def projects():
    domain   = request.args.get('domain', '')
    query    = Project.query
    if domain:
        query = query.filter_by(domain=domain)
    all_projects = query.order_by(Project.created_at.desc()).all()
    domains = db.session.query(Project.domain).distinct().all()
    domains = [d[0] for d in domains]
    return render_template('public/projects.html', projects=all_projects, domains=domains, selected=domain)


@public_bp.route('/internships', methods=['GET', 'POST'])
def internships():
    if request.method == 'POST':
        app_obj = InternshipApplication(
            name            = request.form.get('name','').strip(),
            email           = request.form.get('email','').strip(),
            phone           = request.form.get('phone','').strip(),
            college         = request.form.get('college','').strip(),
            location        = request.form.get('location','').strip(),
            domain          = request.form.get('domain','').strip(),
            internship_type = request.form.get('internship_type','unpaid'),
            message         = request.form.get('message','').strip(),
        )
        db.session.add(app_obj)
        db.session.commit()
        notify_new_internship(app_obj.name, app_obj.college, app_obj.domain, app_obj.internship_type)
        flash('Application submitted! We will contact you soon.', 'success')
        return redirect(url_for('public.internships'))
    return render_template('public/internships.html')


@public_bp.route('/contact', methods=['POST'])
def contact():
    name    = request.form.get('name','').strip()
    email   = request.form.get('email','').strip()
    message = request.form.get('message','').strip()
    if name and email and message:
        cm = ContactMessage(name=name, email=email, message=message)
        db.session.add(cm)
        db.session.commit()
        notify_contact(name, email)
        flash('Message sent! We will get back to you soon.', 'success')
    else:
        flash('Please fill all fields.', 'danger')
    return redirect(url_for('public.index') + '#contact')
