import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # =========================
    # CORE
    # =========================
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret')

    # =========================
    # DATABASE CONFIG (Aiven)
    # =========================
    raw_db_url = os.environ.get("DATABASE_URL")

    if not raw_db_url:
        raise ValueError("DATABASE_URL is not set")

    # Fix driver: mysql:// → mysql+pymysql://
    if raw_db_url.startswith("mysql://"):
        raw_db_url = raw_db_url.replace("mysql://", "mysql+pymysql://", 1)

    # ✅ DO NOT REMOVE ssl-mode (Aiven requires it)
    SQLALCHEMY_DATABASE_URI = raw_db_url

    # ✅ Correct SSL config for Aiven
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "ssl": {
                "ssl_mode": "REQUIRED"
            }
        },
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =========================
    # MAIL CONFIG
    # =========================
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # =========================
    # TELEGRAM (OPTIONAL)
    # =========================
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')

    # =========================
    # ADMIN
    # =========================
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
