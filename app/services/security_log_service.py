from flask import request

from app.extensions import db
from app.models import SecurityLog, LoginAttempt


def create_security_log(
    event_type,
    description,
    user_id=None,
    severity="INFO"
):
    log = SecurityLog(
        user_id=user_id,
        event_type=event_type,
        description=description,
        ip_address=request.remote_addr,
        severity=severity
    )

    db.session.add(log)
    db.session.commit()

    return log


def record_login_attempt(
    email,
    success,
    user_id=None,
    reason=None
):
    attempt = LoginAttempt(
        user_id=user_id,
        email=email,
        ip_address=request.remote_addr,
        user_agent=request.headers.get(
            "User-Agent",
            ""
        )[:500],
        success=success,
        reason=reason
    )

    db.session.add(attempt)
    db.session.commit()

    return attempt