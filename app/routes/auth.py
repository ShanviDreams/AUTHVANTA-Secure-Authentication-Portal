from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)
from urllib.parse import urlsplit

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app.extensions import limiter

from app.models import User

from app.services.password_service import (
    hash_password,
    validate_password_strength
)

from app.services.auth_service import (
    authenticate_user
)

from app.services.email_verification_service import (
    create_verification_token,
    get_verification_record,
    invalidate_verification_tokens
)

from app.services.email_service import (
    send_verification_email
)

from app.services.security_log_service import (
    create_security_log
)

from app.extensions import db


auth_bp = Blueprint(
    "auth",
    __name__
)


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
@limiter.limit(
    "5 per minute",
    methods=["POST"]
)
def login():

    if current_user.is_authenticated:
        target = request.args.get("next")
        if target:
            parsed = urlsplit(target)
            if not parsed.netloc or parsed.netloc == request.host:
                return redirect(target)
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        user, error_message = authenticate_user(
            email,
            password
        )

        if error_message:

            flash(
                error_message,
                "error"
            )

            return render_template(
                "auth/login.html"
            ), 401

        next_url = (
            request.form.get("next", "").strip()
            or session.get("post_login_next", "")
        )

        if next_url:
            parsed = urlsplit(next_url)
            if parsed.scheme not in ("", "http", "https"):
                next_url = ""
            elif parsed.netloc and parsed.netloc != request.host:
                next_url = ""

        session.clear()
        if next_url:
            session["post_login_next"] = next_url

        from app.services.mfa_service import (
            get_mfa_record
        )

        mfa_record = get_mfa_record(
            user.id
        )

        if (
            mfa_record is not None
            and mfa_record.enabled
        ):

            session["mfa_pending_user_id"] = user.id

            create_security_log(
                event_type="MFA_REQUIRED",
                description=(
                    "Password verified. "
                    "MFA verification required."
                ),
                user_id=user.id,
                severity="INFO"
            )

            return redirect(
                url_for(
                    "mfa.challenge"
                )
            )

        login_user(
            user,
            remember=False
        )

        create_security_log(
            event_type="LOGIN_SUCCESS",
            description=(
                "User successfully authenticated."
            ),
            user_id=user.id,
            severity="INFO"
        )

        flash(
            "Login successful.",
            "success"
        )

        target = session.pop("post_login_next", None)
        return redirect(target or url_for("dashboard.dashboard"))

    return render_template(
        "auth/login.html",
        next=request.args.get("next", "")
    )


# --------------------------------------------------
# REGISTER
# --------------------------------------------------

@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if current_user.is_authenticated:
        target = request.args.get("next")
        if target:
            parsed = urlsplit(target)
            if not parsed.netloc or parsed.netloc == request.host:
                return redirect(target)
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        if not username:

            flash(
                "Username is required.",
                "error"
            )

            return render_template(
                "auth/register.html"
            ), 400

        if not email:

            flash(
                "Email address is required.",
                "error"
            )

            return render_template(
                "auth/register.html"
            ), 400

        if not validate_password_strength(
            password
        ):

            flash(
                (
                    "Password must contain at least "
                    "8 characters with uppercase, "
                    "lowercase, number and special character."
                ),
                "error"
            )

            return render_template(
                "auth/register.html"
            ), 400

        existing_username = User.query.filter_by(
            username=username
        ).first()

        if existing_username:

            flash(
                "Username is already registered.",
                "error"
            )

            return render_template(
                "auth/register.html"
            ), 400

        existing_email = User.query.filter_by(
            email=email
        ).first()

        if existing_email:

            flash(
                "Email is already registered.",
                "error"
            )

            return render_template(
                "auth/register.html"
            ), 400

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(
                password
            ),
            role="USER",
            email_verified=False
        )

        db.session.add(user)

        db.session.commit()

        token = create_verification_token(
            user.id
        )

        verification_link = url_for(
            "auth.verify_email",
            token=token,
            _external=True
        )

        try:

            send_verification_email(
                user.email,
                verification_link
            )

            flash(
                (
                    "Account created successfully. "
                    "Please check your email to verify your account."
                ),
                "success"
            )

        except Exception:

            flash(
                (
                    "Account created, but the verification email "
                    "could not be sent."
                ),
                "error"
            )

        return redirect(
            url_for(
                "auth.login"
            )
        )

    return render_template(
        "auth/register.html"
    )


# --------------------------------------------------
# RESEND VERIFICATION EMAIL
# --------------------------------------------------

@auth_bp.route(
    "/resend-verification",
    methods=["POST"]
)
@limiter.limit(
    "3 per 15 minutes",
    methods=["POST"]
)
def resend_verification():

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    if email:

        user = User.query.filter_by(
            email=email
        ).first()

        if (
            user is not None
            and not user.email_verified
        ):

            invalidate_verification_tokens(
                user.id
            )

            token = create_verification_token(
                user.id
            )

            verification_link = url_for(
                "auth.verify_email",
                token=token,
                _external=True
            )

            try:

                send_verification_email(
                    user.email,
                    verification_link
                )

                create_security_log(
                    event_type="VERIFICATION_RESENT",
                    description=(
                        "A new email verification link "
                        "was sent."
                    ),
                    user_id=user.id,
                    severity="INFO"
                )

            except Exception:

                create_security_log(
                    event_type="VERIFICATION_EMAIL_FAILED",
                    description=(
                        "The verification email could "
                        "not be sent."
                    ),
                    user_id=user.id,
                    severity="WARNING"
                )

    flash(
        (
            "If the account exists and is not verified, "
            "a new verification email has been sent."
        ),
        "success"
    )

    return redirect(
        url_for(
            "auth.login"
        )
    )


# --------------------------------------------------
# EMAIL VERIFICATION
# --------------------------------------------------

@auth_bp.route(
    "/verify-email/<token>"
)
def verify_email(token):

    record = get_verification_record(
        token
    )

    if record is None:

        flash(
            (
                "Verification link is invalid or expired. "
                "Please request a new verification email."
            ),
            "error"
        )

        return redirect(
            url_for(
                "auth.login"
            )
        )

    user = db.session.get(
        User,
        record.user_id
    )

    if user is None:

        flash(
            "User account could not be found.",
            "error"
        )

        return redirect(
            url_for(
                "auth.login"
            )
        )

    user.email_verified = True

    from datetime import datetime, timezone

    record.used_at = datetime.now(timezone.utc).replace(tzinfo=None)

    db.session.commit()

    create_security_log(
        event_type="EMAIL_VERIFIED",
        description=(
            "User email address verified successfully."
        ),
        user_id=user.id,
        severity="INFO"
    )

    flash(
        "Email verified successfully. You can now login.",
        "success"
    )

    return redirect(
        url_for(
            "auth.login"
        )
    )


# --------------------------------------------------
# SECURE LOGOUT
# --------------------------------------------------

@auth_bp.route(
    "/logout",
    methods=["POST"]
)
@login_required
def logout():

    user_id = current_user.id

    create_security_log(
        event_type="LOGOUT",
        description=(
            "User logged out successfully."
        ),
        user_id=user_id,
        severity="INFO"
    )

    logout_user()

    session.clear()

    flash(
        "You have been logged out securely.",
        "success"
    )

    return redirect(
        url_for(
            "auth.login"
        )
    )