import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()


def _find_ca_bundle():
    """Return the best available CA bundle path for Aiven SSL."""
    candidates = [
        "/etc/ssl/certs/ca-certificates.crt",   # Debian/Ubuntu (Render)
        "/etc/pki/tls/certs/ca-bundle.crt",     # RHEL/CentOS
        "/etc/ssl/ca-bundle.pem",               # OpenSUSE
        "/usr/local/etc/openssl/cert.pem",      # macOS Homebrew
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Patch SSL CA path dynamically
    ca = _find_ca_bundle()
    if ca:
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            app.config['SQLALCHEMY_DATABASE_URI']
            .split("?")[0] + f"?ssl_ca={ca}"
        )
        app.config['SQLALCHEMY_ENGINE_OPTIONS']['connect_args']['ssl']['ssl_ca'] = ca
    else:
        # No CA found — connect without client-side CA verification (Aiven still encrypts)
        uri = app.config['SQLALCHEMY_DATABASE_URI'].split("?")[0]
        app.config['SQLALCHEMY_DATABASE_URI'] = uri
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            "connect_args": {"ssl": {"ssl_mode": "REQUIRED"}},
            "pool_pre_ping": True,
            "pool_recycle": 280,
        }

    db.init_app(app)
    mail.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    # Register blueprints
    from app.routes.public  import public_bp
    from app.routes.auth    import auth_bp
    from app.routes.user    import user_bp
    from app.routes.admin   import admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp,  url_prefix='/auth')
    app.register_blueprint(user_bp,  url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Auto-create tables
    with app.app_context():
        db.create_all()
        _seed_admin(app)

    return app


def _seed_admin(app):
    """Create default admin if not exists."""
    from app.models import User
    admin_email = app.config['ADMIN_EMAIL']
    admin_pass  = app.config['ADMIN_PASSWORD']
    if not User.query.filter_by(email=admin_email).first():
        admin = User(name='Admin', email=admin_email, is_verified=True, is_admin=True)
        admin.set_password(admin_pass)
        db.session.add(admin)
        db.session.commit()
        print(f"[NewStar] Admin created: {admin_email}")
