
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY is missing. Configure it in your environment."
        )

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    if not all([DB_NAME, DB_USER, DB_PASSWORD]):
        raise RuntimeError(
            "Database configuration is incomplete. "
            "Check DB_NAME, DB_USER, and DB_PASSWORD."
        )

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://"
        f"{DB_USER}:{quote_plus(DB_PASSWORD)}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RATELIMIT_STORAGE_URI = os.getenv(
        "RATELIMIT_STORAGE_URI",
        "memory://"
    )

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = (
        os.getenv("SESSION_COOKIE_SECURE", "0") == "1"
    )
    PERMANENT_SESSION_LIFETIME = 1800

    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
