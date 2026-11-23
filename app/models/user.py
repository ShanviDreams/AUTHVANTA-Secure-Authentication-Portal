from datetime import datetime, timezone

from flask_login import UserMixin

from app.extensions import db


class User(UserMixin, db.Model):

    __tablename__ = "users"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )


    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )


    password_hash = db.Column(
        db.String(255),
        nullable=False
    )


    role = db.Column(
        db.String(20),
        nullable=False,
        default="USER"
    )


    email_verified = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )


    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )