import os


from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

from flask_limiter import Limiter

from flask_limiter.util import get_remote_address

from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()


login_manager = LoginManager()


login_manager.login_view = "auth.login"


login_manager.login_message = (
    "Please login to access this page."
)


login_manager.session_protection = "strong"


limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=os.getenv(
        "RATELIMIT_STORAGE_URI",
        "memory://"
    ),
    headers_enabled=True
)


csrf = CSRFProtect()