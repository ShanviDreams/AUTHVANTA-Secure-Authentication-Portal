from datetime import datetime, timezone
from app.extensions import db


class LoginAttempt(db.Model):
    __tablename__ = "login_attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )
    email = db.Column(db.String(120), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    success = db.Column(db.Boolean, nullable=False, default=False)
    reason = db.Column(db.String(255), nullable=True)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )