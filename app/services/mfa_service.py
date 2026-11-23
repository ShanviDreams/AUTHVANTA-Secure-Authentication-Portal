import base64
import io

import pyotp
import qrcode

from app.extensions import db
from app.models import MFASecret


def create_mfa_secret(user_id):

    existing = MFASecret.query.filter_by(
        user_id=user_id
    ).first()

    if existing:
        return existing.secret

    secret = pyotp.random_base32()

    mfa_record = MFASecret(
        user_id=user_id,
        secret=secret,
        enabled=False
    )

    db.session.add(mfa_record)
    db.session.commit()

    return secret


def get_mfa_record(user_id):

    return MFASecret.query.filter_by(
        user_id=user_id
    ).first()


def generate_mfa_code(secret):

    totp = pyotp.TOTP(secret)

    return totp.now()


def verify_mfa_code(secret, code):

    if not code:
        return False

    totp = pyotp.TOTP(secret)

    return totp.verify(
        code,
        valid_window=1
    )


def get_provisioning_uri(secret, username):

    totp = pyotp.TOTP(secret)

    return totp.provisioning_uri(
        name=username,
        issuer_name="AUTHVANTA"
    )


def generate_qr_code(provisioning_uri):

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=4
    )

    qr.add_data(provisioning_uri)

    qr.make(
        fit=True
    )

    image = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    image_bytes = io.BytesIO()

    image.save(
        image_bytes,
        format="PNG"
    )

    encoded_image = base64.b64encode(
        image_bytes.getvalue()
    ).decode("utf-8")

    return f"data:image/png;base64,{encoded_image}"


def enable_mfa(user_id):

    record = get_mfa_record(user_id)

    if record is None:
        return False

    record.enabled = True

    db.session.commit()

    return True


def disable_mfa(user_id):

    record = get_mfa_record(user_id)

    if record is None:
        return False

    db.session.delete(record)

    db.session.commit()

    return True