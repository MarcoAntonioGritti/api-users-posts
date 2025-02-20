from http import HTTPStatus

from apirestfull_curso.src.controllers.auth import _check_valid_password
from apirestfull_curso.src.models.base import db
from apirestfull_curso.src.models.role import Role
from apirestfull_curso.src.models.user import User


def test_created_token_success(client, create_user_test):
    user = create_user_test

    login_data = {
        "username": user.username,
        "password": "123",  # Supondo que a senha do usuário de teste seja "password123"
    }

    # Faz a requisição de login
    response = client.post("/auth/login", json=login_data)

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json


def test_login_invalid_username(client, create_user_test):
    user = create_user_test

    login_data = {
        "username": "name",
        "password": "123",  # Supondo que a senha do usuário de teste seja "password123"
    }

    # Faz a requisição de login
    response = client.post("/auth/login", json=login_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json == {"message": "Bad username or password"}


def test_login_invalid_password(client, create_user_test):
    user = create_user_test

    login_data = {
        "username": user.username,
        "password": "1234   ",  # Supondo que a senha do usuário de teste seja "password123"
    }

    # Faz a requisição de login
    response = client.post("/auth/login", json=login_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json == {"message": "Bad username or password"}
