from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from email_validator import (
    validate_email,
    EmailNotValidError
)

from app.extensions import db

from app.models import User

from app.services.password_service import (
    hash_password,
    validate_password_strength
)

from app.services.password_reset_service import (
    create_password_reset_token,
    get_password_reset_record
)

from app.services.email_service import (
    send_password_reset_email
)


password_reset_bp = Blueprint(
    "password_reset",
    __name__,
    url_prefix="/password"
)


@password_reset_bp.route(
    "/forgot",
    methods=["GET", "POST"]
)
def forgot_password():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        if not email:

            flash(
                "Please enter your email address.",
                "error"
            )

            return redirect(
                url_for(
                    "password_reset.forgot_password"
                )
            )

        try:

            validated_email = validate_email(
                email,
                check_deliverability=False
            )

            email = validated_email.normalized

        except EmailNotValidError:

            flash(
                "Please enter a valid email address.",
                "error"
            )

            return redirect(
                url_for(
                    "password_reset.forgot_password"
                )
            )

        user = User.query.filter_by(
            email=email
        ).first()

        if user:

            token = create_password_reset_token(
                user.id
            )

            reset_url = url_for(
                "password_reset.reset_password",
                token=token,
                _external=True
            )

            try:

                send_password_reset_email(
                    recipient_email=user.email,
                    reset_link=reset_url
                )

            except Exception:

                flash(
                    "Unable to send the password reset email. "
                    "Please try again later.",
                    "error"
                )

                return redirect(
                    url_for("auth.login")
                )

        flash(
            "If an account exists with that email, "
            "a password reset link has been sent.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "password/forgot_password.html"
    )


@password_reset_bp.route(
    "/reset/<token>",
    methods=["GET", "POST"]
)
def reset_password(token):

    record = get_password_reset_record(
        token
    )

    if record is None:

        flash(
            "Invalid or expired password reset link.",
            "error"
        )

        return redirect(
            url_for("auth.login")
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
            url_for("auth.login")
        )

    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return redirect(
                url_for(
                    "password_reset.reset_password",
                    token=token
                )
            )

        if not validate_password_strength(
            password
        ):

            flash(
                "Password must contain at least "
                "8 characters, including uppercase, "
                "lowercase, number and special character.",
                "error"
            )

            return redirect(
                url_for(
                    "password_reset.reset_password",
                    token=token
                )
            )

        user.password_hash = hash_password(
            password
        )

        record.used_at = db.func.now()

        db.session.commit() 
    

        return render_template(
            "password/reset_success.html"
        )

    return render_template(
        "password/reset_password.html"
    )