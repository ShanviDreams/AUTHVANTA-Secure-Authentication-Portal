from flask import Blueprint, redirect, request, url_for, render_template
from flask_login import current_user

from app.extensions import csrf
from app.services.oauth_server import authorization_server

oauth_bp = Blueprint("oauth", __name__, url_prefix="/oauth")


@oauth_bp.route("/authorize", methods=["GET", "POST"])
def authorize():
    if not current_user.is_authenticated:
        return redirect(
            url_for("auth.login", next=request.url)
        )

    if request.method == "GET":
        grant = authorization_server.get_consent_grant(
            end_user=current_user
        )
        return render_template(
            "oauth_consent.html",
            grant=grant
        )

    if request.form.get("confirm") != "yes":
        return authorization_server.create_authorization_response(
            grant_user=None
        )

    return authorization_server.create_authorization_response(
        grant_user=current_user
    )


@oauth_bp.route("/token", methods=["POST"])
@csrf.exempt
def issue_token():
    return authorization_server.create_token_response()
