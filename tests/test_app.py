
from app import create_app

from app.services.password_service import (
    hash_password,
    verify_password,
    validate_password_strength,
)


def test_app_starts():
    """The Flask application factory should create an app."""
    app = create_app()
    assert app is not None
    assert app.name == "app"


def test_login_page_loads():
    """The login page should respond successfully."""
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/login")
        assert response.status_code == 200


def test_admin_login_page_loads():
    """The admin login page should respond successfully."""
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/admin/login")
        assert response.status_code == 200


def test_user_dashboard_requires_login():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/dashboard/")
        assert response.status_code in (302, 401)


def test_admin_dashboard_requires_login():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/admin/")
        assert response.status_code in (302, 401)


def test_login_post_without_csrf_token_is_rejected():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.post(
            "/login",
            data={
                "username": "test_user",
                "password": "WrongPassword123!",
            },
        )
        assert response.status_code == 400


def test_password_is_hashed():
    password = "SecurePass123!"
    password_hash = hash_password(password)

    assert password_hash != password
    assert password_hash.startswith("$argon2id$")


def test_correct_password_verifies():
    password = "SecurePass123!"
    password_hash = hash_password(password)

    assert verify_password(password, password_hash) is True


def test_wrong_password_is_rejected():
    password_hash = hash_password("SecurePass123!")

    assert verify_password("WrongPass123!", password_hash) is False


def test_password_strength_validation():
    assert validate_password_strength("SecurePass123!") is True
    assert validate_password_strength("weak") is False




def test_login_rate_limit():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    # Reset in-memory limiter state before this isolated test.
    from app.extensions import limiter
    limiter.reset()

    with app.test_client() as client:
        statuses = []

        for _ in range(6):
            response = client.post(
                "/login",
                data={
                    "email": "invalid@example.com",
                    "password": "WrongPassword123!",
                },
                follow_redirects=False,
            )
            statuses.append(response.status_code)

        assert statuses[:5] == [401, 401, 401, 401, 401]
        assert statuses[5] == 429
