import os
import smtplib
from html import escape
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def send_email(recipient_email, subject, html_content, text_content):
    mail_host = os.getenv("MAIL_HOST", "smtp.gmail.com")
    mail_port = int(os.getenv("MAIL_PORT", "587"))
    mail_username = os.getenv("MAIL_USERNAME")
    mail_password = os.getenv("MAIL_PASSWORD")
    mail_from = os.getenv("MAIL_FROM")
    mail_from_name = os.getenv("MAIL_FROM_NAME", "AUTHVANTA")

    required_settings = [mail_username, mail_password, mail_from]

    if not all(required_settings):
        raise ValueError("Gmail SMTP configuration is missing.")

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = f"{mail_from_name} <{mail_from}>"
    message["To"] = recipient_email
    message.set_content(text_content)
    message.add_alternative(html_content, subtype="html")

    with smtplib.SMTP(mail_host, mail_port, timeout=30) as server:
        server.starttls()
        server.login(mail_username, mail_password)
        server.send_message(message)


def email_template(title, heading, message, button_text, action_link, note):
    safe_link = escape(action_link, quote=True)

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(title)}</title>
</head>
<body style="margin:0;padding:30px 12px;background:#f7f5f1;font-family:Arial,sans-serif;color:#25231f;">
    <div style="max-width:560px;margin:20px auto;background:#ffffff;border:1px solid #e9e3d9;border-radius:16px;overflow:hidden;">
        <div style="padding:30px 25px;text-align:center;background:#fff0d9;">
            <h1 style="margin:0;color:#e98516;font-size:28px;">AUTHVANTA</h1>
            <p style="margin:8px 0 0;color:#777168;font-size:14px;">Secure Identity. Smarter Access.</p>
        </div>
        <div style="padding:32px 28px;">
            <h2 style="margin:0 0 18px;color:#25231f;">{escape(heading)}</h2>
            <p style="font-size:15px;line-height:1.7;color:#777168;">{escape(message)}</p>
            <div style="text-align:center;margin:30px 0;">
                <a href="{safe_link}" style="display:inline-block;padding:14px 30px;background:#e98516;color:#ffffff;text-decoration:none;border-radius:8px;font-weight:bold;">{escape(button_text)}</a>
            </div>
            <p style="font-size:13px;line-height:1.6;color:#777168;">{escape(note)}</p>
            <p style="font-size:13px;line-height:1.6;color:#777168;">If you did not request this action, you can safely ignore this email.</p>
        </div>
        <div style="padding:22px;text-align:center;background:#fffaf2;border-top:1px solid #e9e3d9;">
            <p style="margin:0;color:#777168;font-size:12px;line-height:1.7;">
                AUTHVANTA<br>
                Secure Identity. Smarter Access.<br>
                Developed by Shanvi Lakhwan<br>
                BE Computer Science Engineering
            </p>
            <p style="margin:10px 0 0;color:#777168;font-size:11px;">This is an automated security email. Please do not reply.</p>
        </div>
    </div>
</body>
</html>
"""


def send_verification_email(recipient_email, verification_link):
    html_content = email_template(
        title="Verify Your AUTHVANTA Account",
        heading="Verify Your Email",
        message="Thank you for creating your AUTHVANTA account. Please verify your email address by clicking the button below.",
        button_text="VERIFY EMAIL",
        action_link=verification_link,
        note="This verification link is valid for a limited time."
    )

    text_content = f"""
AUTHVANTA
Secure Identity. Smarter Access.

Verify Your Email

Thank you for creating your AUTHVANTA account.

Please verify your email address using this link:

{verification_link}

If you did not create this account, you can safely ignore this email.

This verification link is valid for a limited time.

Developed by Shanvi Lakhwan
BE Computer Science Engineering
"""

    send_email(
        recipient_email,
        "AUTHVANTA | Verify Your Email",
        html_content,
        text_content
    )


def send_password_reset_email(recipient_email, reset_link):
    html_content = email_template(
        title="Reset Your AUTHVANTA Password",
        heading="Password Reset Request",
        message="A password reset was requested for your AUTHVANTA account. Click the button below to create a new password.",
        button_text="RESET PASSWORD",
        action_link=reset_link,
        note="This password reset link is valid for a limited time."
    )

    text_content = f"""
AUTHVANTA
Secure Identity. Smarter Access.

Password Reset Request

A password reset was requested for your AUTHVANTA account.

Use this link to create a new password:

{reset_link}

This password reset link is valid for a limited time.

If you did not request a password reset, you can safely ignore this email.

Developed by Shanvi Lakhwan
BE Computer Science Engineering
"""

    send_email(
        recipient_email,
        "AUTHVANTA | Password Reset",
        html_content,
        text_content
    )
