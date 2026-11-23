
import getpass
import re

from app import create_app
from app.extensions import db
from app.models import User
from app.services.password_service import (
    hash_password,
    validate_password_strength,
)

ADMIN_EMAIL = "authvanta.security@gmail.com"
ADMIN_USERNAME = "authvanta_admin"


def main():
    app = create_app()

    with app.app_context():
        existing_user = User.query.filter_by(
            email=ADMIN_EMAIL
        ).first()

        if existing_user:
            print("An account with this email already exists.")
            print("No changes were made.")
            return

        username_user = User.query.filter_by(
            username=ADMIN_USERNAME
        ).first()

        if username_user:
            print("The admin username is already taken.")
            print("No changes were made.")
            return

        print("AUTHVANTA - Secure Admin Account Setup")
        print("Email:", ADMIN_EMAIL)
        print("Choose a strong, unique password.")
        print("Password must contain uppercase, lowercase,")
        print("a number, a special character, and 8+ characters.")
        print()

        password = getpass.getpass("Create admin password: ")
        confirm_password = getpass.getpass("Confirm admin password: ")

        if password != confirm_password:
            print("Passwords do not match. No account created.")
            return

        if not validate_password_strength(password):
            print("Password does not meet the required strength.")
            print("No account created.")
            return

        confirmation = input(
            "Type CREATE ADMIN to confirm account creation: "
        ).strip()

        if confirmation != "CREATE ADMIN":
            print("Cancelled. No account created.")
            return

        admin = User(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password_hash=hash_password(password),
            role="ADMIN",
            email_verified=False,
        )

        try:
            db.session.add(admin)
            db.session.commit()
            print()
            print("Admin account created successfully.")
            print("Role: ADMIN")
            print("Email verified: No")
            print("Next: complete email verification and MFA setup.")
        except Exception:
            db.session.rollback()
            print("Account creation failed. Database changes rolled back.")
            raise


if __name__ == "__main__":
    main()
