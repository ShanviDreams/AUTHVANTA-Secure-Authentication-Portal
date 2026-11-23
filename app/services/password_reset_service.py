import hashlib

import secrets

from datetime import (
    timezone,
    datetime,
    timedelta
)

from app.extensions import db

from app.models import PasswordResetToken


RESET_EXPIRY_MINUTES = 15


def create_password_reset_token(
    user_id
):

    token = secrets.token_urlsafe(32)

    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    reset_record = PasswordResetToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=(
            datetime.now(timezone.utc).replace(tzinfo=None)
            + timedelta(
                minutes=RESET_EXPIRY_MINUTES
            )
        )
    )

    db.session.add(
        reset_record
    )

    db.session.commit()

    return token


def get_password_reset_record(
    token
):

    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    record = (
        PasswordResetToken.query
        .filter_by(
            token_hash=token_hash
        )
        .first()
    )

    if record is None:
        return None

    if record.used_at is not None:
        return None

    if datetime.now(timezone.utc).replace(tzinfo=None) > record.expires_at:
        return None

    return record