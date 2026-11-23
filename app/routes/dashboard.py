from flask import (
    Blueprint,
    render_template
)

from flask_login import (
    login_required,
    current_user
)

from app.models import (
    MFASecret,
    LoginAttempt,
    SecurityLog
)


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard_bp.route("/")
@login_required
def dashboard():

    mfa_record = MFASecret.query.filter_by(
        user_id=current_user.id
    ).first()

    recent_attempts = LoginAttempt.query.filter_by(
        user_id=current_user.id
    ).order_by(
        LoginAttempt.created_at.desc()
    ).limit(5).all()

    recent_logs = SecurityLog.query.filter_by(
        user_id=current_user.id
    ).order_by(
        SecurityLog.created_at.desc()
    ).limit(5).all()

    return render_template(
        "dashboard/dashboard.html",
        mfa_enabled=(
            mfa_record is not None
            and mfa_record.enabled
        ),
        recent_attempts=recent_attempts,
        recent_logs=recent_logs
    )


@dashboard_bp.route("/profile")
@login_required
def profile():

    return render_template(
        "dashboard/profile.html"
    )