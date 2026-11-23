from app.models import User
from app.services.password_service import verify_password
from app.services.security_log_service import (
    record_login_attempt,
    create_security_log
)


def authenticate_user(email, password):
    user = User.query.filter_by(
        email=email
    ).first()

    if user is None:
        record_login_attempt(
            email=email,
            success=False,
            reason="User not found"
        )

        create_security_log(
            event_type="LOGIN_FAILED",
            description="Login attempt with unknown email.",
            severity="WARNING"
        )

        return None, "Invalid email or password."

    if not verify_password(
        password,
        user.password_hash
    ):
        record_login_attempt(
            email=email,
            success=False,
            user_id=user.id,
            reason="Invalid password"
        )

        create_security_log(
            event_type="LOGIN_FAILED",
            description="Invalid password entered.",
            user_id=user.id,
            severity="WARNING"
        )

        return None, "Invalid email or password."

    if not user.email_verified:
        record_login_attempt(
            email=email,
            success=False,
            user_id=user.id,
            reason="Email not verified"
        )

        create_security_log(
            event_type="LOGIN_BLOCKED",
            description="Login blocked because email is not verified.",
            user_id=user.id,
            severity="WARNING"
        )

        return None, "Please verify your email before logging in."

    record_login_attempt(
        email=email,
        success=True,
        user_id=user.id,
        reason="Password verified"
    )

    return user, None