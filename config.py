import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret')

    # =========================
    # DATABASE CONFIG (Aiven)
    # =========================
    raw_db_url = os.environ.get("DATABASE_URL")

    if not raw_db_url:
        raise ValueError("DATABASE_URL is not set in .env")

    # Fix driver: mysql:// → mysql+pymysql://
    if raw_db_url.startswith("mysql://"):
        raw_db_url = raw_db_url.replace("mysql://", "mysql+pymysql://", 1)

    # Optional: remove ssl-mode (handled separately)
    if "?ssl-mode=" in raw_db_url:
        raw_db_url = raw_db_url.split("?")[0]

    SQLALCHEMY_DATABASE_URI = raw_db_url

    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "ssl": {
                # ⚠️ Windows note: this path may not exist
                # You can comment this if SSL errors occur
                "ssl_ca": "/etc/ssl/certs/ca-certificates.crt"
            }
        },
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =========================
    # MAIL CONFIG
    # =========================
    MAIL_SERVER   = 'smtp.gmail.com'
    MAIL_PORT     = 587
    MAIL_USE_TLS  = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # =========================
    # TELEGRAM
    # =========================
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID   = os.environ.get('TELEGRAM_CHAT_ID', '')

    # =========================
    # ADMIN
    # =========================
    ADMIN_EMAIL    = os.environ.get('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')