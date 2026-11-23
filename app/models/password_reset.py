from datetime import datetime, timezone

from app.extensions import db


class PasswordResetToken(db.Model):

    __tablename__ = "password_reset_tokens"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    token_hash = db.Column(
        db.String(64),
        unique=True,
        nullable=False
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )

    used_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )