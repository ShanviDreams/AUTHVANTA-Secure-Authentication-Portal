from datetime import datetime, timezone

from app.extensions import db


class MFASecret(db.Model):

    __tablename__ = "mfa_secrets"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    secret = db.Column(
        db.String(64),
        nullable=False
    )

    enabled = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )