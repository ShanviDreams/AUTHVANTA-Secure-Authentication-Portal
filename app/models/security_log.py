from datetime import datetime, timezone
from app.extensions import db


class SecurityLog(db.Model):
    __tablename__ = "security_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )
    event_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)
    severity = db.Column(
        db.String(20),
        nullable=False,
        default="INFO"
    )
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )