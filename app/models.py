from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(120), nullable=False)
    email       = db.Column(db.String(150), unique=True, nullable=False)
    password    = db.Column(db.String(256), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_admin    = db.Column(db.Boolean, default=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    requests    = db.relationship('Request', backref='user', lazy=True)

    def set_password(self, raw):
        self.password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)


class OTPVerification(db.Model):
    __tablename__ = 'otp_verification'
    id     = db.Column(db.Integer, primary_key=True)
    email  = db.Column(db.String(150), nullable=False)
    otp    = db.Column(db.String(6), nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)


class Project(db.Model):
    __tablename__ = 'projects'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price       = db.Column(db.Float, nullable=False)
    image       = db.Column(db.String(300), default='')
    domain      = db.Column(db.String(100), default='General')
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)


class TeamMember(db.Model):
    __tablename__ = 'team'
    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(150), nullable=False)
    role           = db.Column(db.String(150), nullable=False)
    portfolio_link = db.Column(db.String(300), default='')
    image          = db.Column(db.String(300), default='')
    order_index    = db.Column(db.Integer, default=0)


class Request(db.Model):
    __tablename__ = 'requests'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type       = db.Column(db.Enum('project', 'idea', 'mentorship', 'internship'), nullable=False)
    subject    = db.Column(db.String(300), default='')
    message    = db.Column(db.Text, nullable=False)
    status     = db.Column(db.Enum('pending', 'reviewing', 'accepted', 'rejected'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class InternshipApplication(db.Model):
    __tablename__ = 'internship_applications'
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(150), nullable=False)
    email        = db.Column(db.String(150), nullable=False)
    phone        = db.Column(db.String(20), nullable=False)
    college      = db.Column(db.String(200), nullable=False)
    location     = db.Column(db.String(100), nullable=False)
    domain       = db.Column(db.String(100), nullable=False)
    internship_type = db.Column(db.Enum('paid', 'unpaid'), default='unpaid')
    message      = db.Column(db.Text, default='')
    status       = db.Column(db.Enum('pending', 'reviewing', 'selected', 'rejected'), default='pending')
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)


class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(150), nullable=False)
    email      = db.Column(db.String(150), nullable=False)
    message    = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
