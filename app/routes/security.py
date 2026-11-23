from flask import (
    Blueprint,
    render_template
)

from flask_login import (
    login_required,
    current_user
)

from app.models import SecurityLog


security_bp = Blueprint(
    "security",
    __name__,
    url_prefix="/security"
)


@security_bp.route("/activity")
@login_required
def activity():

    logs = SecurityLog.query.filter_by(
        user_id=current_user.id
    ).order_by(
        SecurityLog.created_at.desc()
    ).limit(50).all()

    return render_template(
        "dashboard/security_activity.html",
        logs=logs
    )