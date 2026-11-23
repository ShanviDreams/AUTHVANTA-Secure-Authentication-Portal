import hashlib
import secrets

from datetime import (
    timezone,
    datetime,
    timedelta
)

from app.extensions import db

from app.models import (
    EmailVerificationToken
)


VERIFICATION_EXPIRY_MINUTES = 15


def invalidate_verification_tokens(user_id):

    active_tokens = EmailVerificationToken.query.filter_by(
        user_id=user_id,
        used_at=None
    ).all()

    for token_record in active_tokens:

        token_record.used_at = datetime.now(timezone.utc).replace(tzinfo=None)

    db.session.commit()


def create_verification_token(user_id):

    token = secrets.token_urlsafe(32)

    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    verification_record = EmailVerificationToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=(
            datetime.now(timezone.utc).replace(tzinfo=None)
            + timedelta(
                minutes=VERIFICATION_EXPIRY_MINUTES
            )
        )
    )

    db.session.add(
        verification_record
    )

    db.session.commit()

    return token


def get_verification_record(token):

    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    record = EmailVerificationToken.query.filter_by(
        token_hash=token_hash
    ).first()

    if record is None:

        return None

    if record.used_at is not None:

        return None

    if datetime.now(timezone.utc).replace(tzinfo=None) > record.expires_at:

        return None

    return record