
from flask import url_for

from app import create_app
from app.extensions import db
from app.models import User
from app.services.email_verification_service import (
    invalidate_verification_tokens,
    create_verification_token,
)
from app.services.email_service import send_verification_email

ADMIN_EMAIL = "authvanta.security@gmail.com"
BASE_URL = "http://127.0.0.1:5000"


def main():
    app = create_app()

    with app.app_context():
        admin = User.query.filter_by(email=ADMIN_EMAIL).first()

        if admin is None or admin.role != "ADMIN":
            print("Admin account not found. No email sent.")
            return

        if admin.email_verified:
            print("Admin email is already verified.")
            return

        invalidate_verification_tokens(admin.id)
        token = create_verification_token(admin.id)

        with app.test_request_context(
            base_url=BASE_URL
        ):
            verification_link = url_for(
                "auth.verify_email",
                token=token,
                _external=True,
            )

        try:
            send_verification_email(
                recipient_email=admin.email,
                verification_link=verification_link,
            )
            print("Verification email sent to:", admin.email)
            print("Open the NEW email and click VERIFY EMAIL.")
            print("Link:", verification_link)
            print("The link expires in 15 minutes.")
        except Exception:
            db.session.rollback()
            print("Email sending failed. Check SMTP settings.")
            raise


if __name__ == "__main__":
    main()
