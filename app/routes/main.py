from flask import (
    Blueprint,
    redirect,
    url_for
)

from flask_login import current_user, login_required

from sqlalchemy import text

from app.extensions import db


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():

    if current_user.is_authenticated:
        return redirect(
            url_for("dashboard.dashboard")
        )

    return redirect(
        url_for("auth.login")
    )


@main_bp.route("/health/db")
def database_health():

    result = db.session.execute(
        text("SELECT 1")
    )

    value = result.scalar()

    return {
        "database": "connected",
        "test_result": value
    }