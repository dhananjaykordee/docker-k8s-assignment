import logging


def test_invalid_credentials_return_unauthorized(isolated_database):
    response = isolated_database.post(
        "/login",
        json={"username": "missing-user", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username or password"}


def test_missing_password_returns_validation_error(isolated_database):
    response = isolated_database.post(
        "/login",
        json={"username": "missing-user"},
    )

    assert response.status_code == 422


def test_invalid_password_input_is_not_logged(isolated_database, caplog):
    caplog.set_level(logging.ERROR, logger="utils.exception_handler")
    secret_marker = "password-that-must-not-be-logged"

    response = isolated_database.post(
        "/login",
        json={"username": "test-user", "password": [secret_marker]},
    )

    assert response.status_code == 422
    assert "('body', 'password')" in caplog.text
    assert secret_marker not in caplog.text
