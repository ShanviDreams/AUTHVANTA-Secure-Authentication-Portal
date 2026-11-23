
import getpass

from app import create_app
from app.extensions import db
from app.models import User
from app.services.mfa_service import (
    create_mfa_secret,
    get_mfa_record,
    get_provisioning_uri,
    generate_qr_code,
    verify_mfa_code,
    enable_mfa,
)
from app.services.security_log_service import create_security_log

ADMIN_EMAIL = "authvanta.security@gmail.com"


def main():
    app = create_app()

    with app.app_context():
        admin = User.query.filter_by(email=ADMIN_EMAIL).first()

        if admin is None or admin.role != "ADMIN":
            print("Verified admin account not found.")
            return

        if not admin.email_verified:
            print("Admin email is not verified. Setup cancelled.")
            return

        record = get_mfa_record(admin.id)

        if record and record.enabled:
            print("Admin MFA is already enabled.")
            return

        secret = create_mfa_secret(admin.id)
        provisioning_uri = get_provisioning_uri(secret, ADMIN_EMAIL)
        qr_code = generate_qr_code(provisioning_uri)

        import base64
        import io
        import qrcode

        image_data = base64.b64decode(qr_code.split(",", 1)[1])
        image = qrcode.make(provisioning_uri)
        image.save("admin_mfa_qr.png")

        print("QR code saved as admin_mfa_qr.png")
        print("Open this image and scan it with your authenticator app.")
        print("Do not share the QR image or secret with anyone.")
        print()

        code = getpass.getpass(
            "Enter the current 6-digit authenticator code: "
        ).strip()

        if not verify_mfa_code(secret, code):
            print("Code verification failed. MFA remains disabled.")
            return

        if enable_mfa(admin.id):
            create_security_log(
                event_type="MFA_ENABLED",
                description="Admin MFA enrollment completed successfully.",
                user_id=admin.id,
                severity="INFO",
            )
            print("Admin MFA enabled successfully.")
        else:
            print("Could not enable MFA.")


if __name__ == "__main__":
    main()
