
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from flask_login import login_required, current_user

from app.extensions import db, limiter
from app.models import User, LoginAttempt, SecurityLog
from app.utils.decorators import admin_required
from app.services.password_service import verify_password
from app.services.mfa_service import get_mfa_record
from app.services.security_log_service import (
    create_security_log,
    record_login_attempt
)

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# --------------------------------------------------
# ADMIN LOGIN
# --------------------------------------------------

@admin_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def login():

    if current_user.is_authenticated:
        if current_user.role == "ADMIN":
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user is None:
            record_login_attempt(
                email=email or "unknown",
                success=False,
                reason="Admin login: account not found"
            )
            create_security_log(
                event_type="ADMIN_LOGIN_FAILED",
                description="Admin login attempted with unknown email.",
                severity="WARNING"
            )
            flash("Admin authentication failed.", "error")
            return render_template("admin/login.html"), 401

        if not verify_password(password, user.password_hash):
            record_login_attempt(
                email=email,
                success=False,
                user_id=user.id,
                reason="Admin login: invalid password"
            )
            create_security_log(
                event_type="ADMIN_LOGIN_FAILED",
                description="Invalid password entered on admin login.",
                user_id=user.id,
                severity="WARNING"
            )
            flash("Admin authentication failed.", "error")
            return render_template("admin/login.html"), 401

        if user.role != "ADMIN" or not user.email_verified:
            record_login_attempt(
                email=email,
                success=False,
                user_id=user.id,
                reason="Admin role or email verification check failed"
            )
            create_security_log(
                event_type="ADMIN_ACCESS_DENIED",
                description="Admin login denied due to account permissions.",
                user_id=user.id,
                severity="WARNING"
            )
            flash("Admin authentication failed.", "error")
            return render_template("admin/login.html"), 401

        mfa_record = get_mfa_record(user.id)

        if mfa_record is None or not mfa_record.enabled:
            create_security_log(
                event_type="ADMIN_MFA_REQUIRED",
                description="Admin login blocked because MFA is not enabled.",
                user_id=user.id,
                severity="WARNING"
            )
            flash(
                "Admin access requires enabled MFA. "
                "Enable MFA for this account before using the Admin Portal.",
                "error"
            )
            return render_template("admin/login.html"), 403

        session.clear()
        session["mfa_pending_user_id"] = user.id
        session["mfa_pending_admin"] = True

        create_security_log(
            event_type="ADMIN_PASSWORD_VERIFIED",
            description="Admin password verified; MFA verification is pending.",
            user_id=user.id,
            severity="INFO"
        )

        return redirect(url_for("mfa.challenge"))

    return render_template("admin/login.html")


# --------------------------------------------------
# ADMIN DASHBOARD
# --------------------------------------------------

@admin_bp.route("/")
@login_required
@admin_required
def dashboard():

    total_users = User.query.count()
    verified_users = User.query.filter_by(
        email_verified=True
    ).count()
    admin_users = User.query.filter_by(
        role="ADMIN"
    ).count()
    failed_logins = LoginAttempt.query.filter_by(
        success=False
    ).count()

    recent_logs = SecurityLog.query.order_by(
        SecurityLog.created_at.desc()
    ).limit(10).all()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        verified_users=verified_users,
        admin_users=admin_users,
        failed_logins=failed_logins,
        recent_logs=recent_logs
    )


# --------------------------------------------------
# USER MANAGEMENT
# --------------------------------------------------

@admin_bp.route("/users")
@login_required
@admin_required
def users():

    users_list = User.query.order_by(
        User.created_at.desc()
    ).all()

    return render_template(
        "admin/users.html",
        users=users_list
    )


# --------------------------------------------------
# SECURITY LOGS
# --------------------------------------------------

@admin_bp.route("/security-logs")
@login_required
@admin_required
def security_logs():

    logs = SecurityLog.query.order_by(
        SecurityLog.created_at.desc()
    ).limit(100).all()

    return render_template(
        "admin/security_logs.html",
        logs=logs
    )


# --------------------------------------------------
# LOGIN ATTEMPTS
# --------------------------------------------------

@admin_bp.route("/login-attempts")
@login_required
@admin_required
def login_attempts():

    attempts = LoginAttempt.query.order_by(
        LoginAttempt.created_at.desc()
    ).limit(100).all()

    return render_template(
        "admin/login_attempts.html",
        attempts=attempts
    )
