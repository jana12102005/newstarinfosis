import requests as req
from flask import current_app
from flask_mail import Message
from app import mail


def send_telegram(text: str):
    token = current_app.config.get('TELEGRAM_BOT_TOKEN', '')
    chat  = current_app.config.get('TELEGRAM_CHAT_ID', '')
    if not token or not chat:
        return
    try:
        req.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat, "text": text, "parse_mode": "HTML"},
            timeout=5
        )
    except Exception as e:
        print(f"[Telegram Error] {e}")


def send_email(to, subject, body):
    try:
        msg = Message(subject, recipients=[to], body=body)
        mail.send(msg)
    except Exception as e:
        print(f"[Mail Error] {e}")


def send_otp_email(to_email, otp):
    subject = "NewStar Infosis – Email Verification OTP"
    body = f"""
Hello from NewStar Infosis!

Your OTP for email verification is: {otp}

This OTP is valid for 10 minutes.

Regards,
NewStar Infosis Team
Namakkal | Chennai | Villupuram, Tamil Nadu
"""
    send_email(to_email, subject, body)


def notify_new_request(name, req_type, subject):
    msg = (
        f"🚀 <b>New {req_type.title()} Request</b>\n"
        f"👤 Name: {name}\n"
        f"📋 Subject: {subject}"
    )
    send_telegram(msg)


def notify_new_user(name, email):
    msg = (
        f"🎉 <b>New User Registered</b>\n"
        f"👤 Name: {name}\n"
        f"📧 Email: {email}"
    )
    send_telegram(msg)


def notify_new_internship(name, college, domain, itype):
    msg = (
        f"🎓 <b>New Internship Application</b>\n"
        f"👤 Name: {name}\n"
        f"🏫 College: {college}\n"
        f"💡 Domain: {domain}\n"
        f"💰 Type: {itype.title()}"
    )
    send_telegram(msg)


def notify_contact(name, email):
    msg = (
        f"📩 <b>New Contact Message</b>\n"
        f"👤 Name: {name}\n"
        f"📧 Email: {email}"
    )
    send_telegram(msg)
