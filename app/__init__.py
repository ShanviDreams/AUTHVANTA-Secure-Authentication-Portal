from flask import (
    Flask,
    flash,
    redirect,
    url_for,
    render_template
)

from flask_wtf.csrf import CSRFError
from app.config import Config
from app.extensions import db, login_manager, limiter, csrf


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    csrf.init_app(app)

    # Initialize OAuth 2.0 server
    from app.services.oauth_server import init_oauth_server
    init_oauth_server(app)

    # Register application blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.mfa import mfa_bp
    from app.routes.password_reset import password_reset_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.admin import admin_bp
    from app.routes.security import security_bp
    from app.routes.oauth import oauth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(mfa_bp)
    app.register_blueprint(password_reset_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(security_bp)
    app.register_blueprint(oauth_bp)

    @app.errorhandler(429)
    def rate_limit_error(error):
        return error.get_response() or (
            render_template(
                "errors/400.html",
                error_message=(
                    "Too many login attempts. "
                    "Please wait before trying again."
                ),
            ),
            429,
        )

    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        return render_template(
            "errors/400.html",
            error_message=(
                "Security validation failed. "
                "Please refresh the page and try again."
            )
        ), 400

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import User

    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None
