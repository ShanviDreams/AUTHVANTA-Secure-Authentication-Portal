from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):

        if not current_user.is_authenticated:
            return redirect(
                url_for("auth.login")
            )

        if current_user.role != "ADMIN":
            flash(
                "Administrator access is required.",
                "error"
            )

            return redirect(
                url_for("dashboard.dashboard")
            )

        return function(*args, **kwargs)

    return decorated_function