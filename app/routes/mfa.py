
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from flask_login import (
    login_required,
    current_user,
    login_user
)

from app.services.mfa_service import (
    create_mfa_secret,
    get_mfa_record,
    get_provisioning_uri,
    generate_qr_code,
    verify_mfa_code,
    enable_mfa,
    disable_mfa
)

from app.models import User
from app.extensions import db

from app.services.security_log_service import create_security_log


mfa_bp = Blueprint(
    "mfa",
    __name__,
    url_prefix="/mfa"
)


# --------------------------------------------------
# MFA SETUP
# --------------------------------------------------

@mfa_bp.route("/setup", methods=["GET", "POST"])
@login_required
def setup():

    record = get_mfa_record(current_user.id)

    if record is None:
        secret = create_mfa_secret(current_user.id)
    else:
        secret = record.secret

    provisioning_uri = get_provisioning_uri(
        secret,
        current_user.username
    )

    qr_code = generate_qr_code(provisioning_uri)

    if request.method == "POST":

        code = request.form.get("code", "").strip()

        if verify_mfa_code(secret, code):

            enable_mfa(current_user.id)

            create_security_log(
                event_type="MFA_ENABLED",
                description="Multi-factor authentication enabled.",
                user_id=current_user.id,
                severity="INFO"
            )

            flash(
                "MFA has been enabled successfully.",
                "success"
            )

            target = session.pop("post_login_next", None)
            return redirect(target or url_for("dashboard.dashboard"))

        flash(
            "Invalid MFA code. Please try again.",
            "error"
        )

    return render_template(
        "auth/mfa.html",
        secret=secret,
        provisioning_uri=provisioning_uri,
        qr_code=qr_code
    )


# --------------------------------------------------
# MFA CHALLENGE
# --------------------------------------------------

@mfa_bp.route("/challenge", methods=["GET", "POST"])
def challenge():

    pending_user_id = session.get("mfa_pending_user_id")
    pending_admin = session.get("mfa_pending_admin", False)

    if not pending_user_id:

        flash(
            "Your MFA session has expired. Please login again.",
            "error"
        )

        return redirect(url_for("auth.login"))

    user = db.session.get(User, pending_user_id)

    if user is None:

        session.clear()

        flash(
            "Authentication session is invalid.",
            "error"
        )

        return redirect(url_for("auth.login"))

    # An admin challenge must remain tied to an ADMIN account.
    if pending_admin and user.role != "ADMIN":

        session.clear()

        create_security_log(
            event_type="ADMIN_MFA_DENIED",
            description="Admin MFA challenge rejected due to invalid role.",
            user_id=user.id,
            severity="WARNING"
        )

        flash("Admin authentication failed.", "error")

        return redirect(url_for("admin.login"))

    record = get_mfa_record(user.id)

    # Never allow an admin challenge to bypass MFA.
    if pending_admin and (
        record is None or not record.enabled
    ):

        session.clear()

        create_security_log(
            event_type="ADMIN_MFA_DENIED",
            description="Admin MFA challenge rejected because MFA is not enabled.",
            user_id=user.id,
            severity="WARNING"
        )

        flash(
            "Admin access requires enabled MFA.",
            "error"
        )

        return redirect(url_for("admin.login"))

    # Regular users without enabled MFA can complete login.
    if record is None or not record.enabled:

        if pending_admin:

            session.clear()

            flash(
                "Admin access requires enabled MFA.",
                "error"
            )

            return redirect(url_for("admin.login"))

        session.clear()

        login_user(user, remember=False)

        create_security_log(
            event_type="LOGIN_SUCCESS",
            description="User authenticated without MFA.",
            user_id=user.id,
            severity="INFO"
        )

        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":

        code = request.form.get("code", "").strip()

        if verify_mfa_code(record.secret, code):

            # Keep the destination before clearing pending MFA state.
            is_admin_login = bool(pending_admin)

            # Re-check authorization immediately before completing login.
            if is_admin_login and user.role != "ADMIN":

                session.clear()

                create_security_log(
                    event_type="ADMIN_MFA_DENIED",
                    description="Admin role check failed during MFA completion.",
                    user_id=user.id,
                    severity="WARNING"
                )

                flash("Admin authentication failed.", "error")

                return redirect(url_for("admin.login"))

            post_login_next = session.get("post_login_next")
            session.clear()
            if post_login_next:
                session["post_login_next"] = post_login_next

            login_user(user, remember=False)

            create_security_log(
                event_type="MFA_SUCCESS",
                description="MFA verification completed successfully.",
                user_id=user.id,
                severity="INFO"
            )

            create_security_log(
                event_type="LOGIN_SUCCESS",
                description=(
                    "Admin completed password and MFA authentication."
                    if is_admin_login
                    else "User completed password and MFA authentication."
                ),
                user_id=user.id,
                severity="INFO"
            )

            flash(
                "MFA verification successful.",
                "success"
            )

            if is_admin_login:
                return redirect(url_for("admin.dashboard"))

            target = session.pop("post_login_next", None)
            return redirect(target or url_for("dashboard.dashboard"))

        create_security_log(
            event_type="MFA_FAILED",
            description="Invalid MFA authentication code entered.",
            user_id=user.id,
            severity="WARNING"
        )

        flash(
            "Invalid authentication code.",
            "error"
        )

    return render_template("auth/mfa_challenge.html")


# --------------------------------------------------
# SECURE MFA DISABLE
# --------------------------------------------------

@mfa_bp.route("/disable", methods=["POST"])
@login_required
def disable():

    success = disable_mfa(current_user.id)

    if success:

        create_security_log(
            event_type="MFA_DISABLED",
            description="Multi-factor authentication disabled.",
            user_id=current_user.id,
            severity="WARNING"
        )

        flash(
            "MFA has been disabled.",
            "success"
        )

    else:

        flash(
            "MFA is already disabled.",
            "error"
        )

    if current_user.role == "ADMIN":
        return redirect(url_for("admin.dashboard"))

    return redirect(url_for("dashboard.dashboard"))
