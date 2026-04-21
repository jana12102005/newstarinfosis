from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import Project, TeamMember, Request, User, InternshipApplication, ContactMessage
from app import db

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    stats = {
        'users':        User.query.count(),
        'projects':     Project.query.count(),
        'requests':     Request.query.count(),
        'pending':      Request.query.filter_by(status='pending').count(),
        'internships':  InternshipApplication.query.count(),
        'contacts':     ContactMessage.query.count(),
    }
    recent_requests = Request.query.order_by(Request.created_at.desc()).limit(10).all()
    return render_template('admin/dashboard.html', stats=stats, recent_requests=recent_requests)


# ── PROJECTS ──────────────────────────────────────────────────────────────────
@admin_bp.route('/projects')
@login_required
@admin_required
def projects():
    all_p = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=all_p)


@admin_bp.route('/projects/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_project():
    if request.method == 'POST':
        p = Project(
            name        = request.form.get('name','').strip(),
            description = request.form.get('description','').strip(),
            price       = float(request.form.get('price', 0)),
            image       = request.form.get('image','').strip(),
            domain      = request.form.get('domain','General').strip(),
        )
        db.session.add(p)
        db.session.commit()
        flash('Project added!', 'success')
        return redirect(url_for('admin.projects'))
    return render_template('admin/project_form.html', project=None)


@admin_bp.route('/projects/edit/<int:pid>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_project(pid):
    p = Project.query.get_or_404(pid)
    if request.method == 'POST':
        p.name        = request.form.get('name','').strip()
        p.description = request.form.get('description','').strip()
        p.price       = float(request.form.get('price', 0))
        p.image       = request.form.get('image','').strip()
        p.domain      = request.form.get('domain','General').strip()
        db.session.commit()
        flash('Project updated!', 'success')
        return redirect(url_for('admin.projects'))
    return render_template('admin/project_form.html', project=p)


@admin_bp.route('/projects/delete/<int:pid>', methods=['POST'])
@login_required
@admin_required
def delete_project(pid):
    p = Project.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    flash('Project deleted.', 'info')
    return redirect(url_for('admin.projects'))


# ── TEAM ──────────────────────────────────────────────────────────────────────
@admin_bp.route('/team')
@login_required
@admin_required
def team():
    members = TeamMember.query.order_by(TeamMember.order_index).all()
    return render_template('admin/team.html', members=members)


@admin_bp.route('/team/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_member():
    if request.method == 'POST':
        m = TeamMember(
            name           = request.form.get('name','').strip(),
            role           = request.form.get('role','').strip(),
            portfolio_link = request.form.get('portfolio_link','').strip(),
            image          = request.form.get('image','').strip(),
            order_index    = int(request.form.get('order_index', 0)),
        )
        db.session.add(m)
        db.session.commit()
        flash('Team member added!', 'success')
        return redirect(url_for('admin.team'))
    return render_template('admin/member_form.html', member=None)


@admin_bp.route('/team/edit/<int:mid>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_member(mid):
    m = TeamMember.query.get_or_404(mid)
    if request.method == 'POST':
        m.name           = request.form.get('name','').strip()
        m.role           = request.form.get('role','').strip()
        m.portfolio_link = request.form.get('portfolio_link','').strip()
        m.image          = request.form.get('image','').strip()
        m.order_index    = int(request.form.get('order_index', 0))
        db.session.commit()
        flash('Member updated!', 'success')
        return redirect(url_for('admin.team'))
    return render_template('admin/member_form.html', member=m)


@admin_bp.route('/team/delete/<int:mid>', methods=['POST'])
@login_required
@admin_required
def delete_member(mid):
    m = TeamMember.query.get_or_404(mid)
    db.session.delete(m)
    db.session.commit()
    flash('Member removed.', 'info')
    return redirect(url_for('admin.team'))


# ── REQUESTS ─────────────────────────────────────────────────────────────────
@admin_bp.route('/requests')
@login_required
@admin_required
def requests():
    filter_type   = request.args.get('type', '')
    filter_status = request.args.get('status', '')
    query = Request.query
    if filter_type:
        query = query.filter_by(type=filter_type)
    if filter_status:
        query = query.filter_by(status=filter_status)
    all_r = query.order_by(Request.created_at.desc()).all()
    return render_template('admin/requests.html', requests=all_r, filter_type=filter_type, filter_status=filter_status)


@admin_bp.route('/requests/update/<int:rid>', methods=['POST'])
@login_required
@admin_required
def update_request(rid):
    r = Request.query.get_or_404(rid)
    r.status = request.form.get('status', r.status)
    db.session.commit()
    flash('Request status updated.', 'success')
    return redirect(url_for('admin.requests'))


# ── INTERNSHIPS ───────────────────────────────────────────────────────────────
@admin_bp.route('/internships')
@login_required
@admin_required
def internships():
    apps = InternshipApplication.query.order_by(InternshipApplication.created_at.desc()).all()
    return render_template('admin/internships.html', apps=apps)


@admin_bp.route('/internships/update/<int:aid>', methods=['POST'])
@login_required
@admin_required
def update_internship(aid):
    a = InternshipApplication.query.get_or_404(aid)
    a.status = request.form.get('status', a.status)
    db.session.commit()
    flash('Internship status updated.', 'success')
    return redirect(url_for('admin.internships'))


# ── USERS ─────────────────────────────────────────────────────────────────────
@admin_bp.route('/users')
@login_required
@admin_required
def users():
    all_u = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=all_u)


# ── CONTACTS ─────────────────────────────────────────────────────────────────
@admin_bp.route('/contacts')
@login_required
@admin_required
def contacts():
    msgs = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/contacts.html', msgs=msgs)
