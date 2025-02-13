from datetime import datetime

import pytest

from apirestfull_curso.src.app import create_app
from apirestfull_curso.src.models.base import db
from apirestfull_curso.src.models.post import Post
from apirestfull_curso.src.models.role import Role
from apirestfull_curso.src.models.user import User


@pytest.fixture()
def app():
    # Cria a aplicação (usará o ambiente definido pela variável de ambiente)
    app = create_app("testing")

    # Entra no contexto da aplicação
    with app.app_context():
        db.create_all()  # Cria todas as tabelas no banco de dados
        yield app  # Retorna a aplicação para o teste


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def access_token_admin(client):
    role = db.session.execute(db.select(Role).where(Role.name == "Admin")).scalar()
    role_id = role.id
    user = User(username="marcola", password="123", role_id=role_id)
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/auth/login", json={"username": user.username, "password": user.password}
    )

    return response.json["access_token"]


@pytest.fixture()
def access_token_normal(client):
    role = Role(name="Normal")
    db.session.add(role)
    db.session.commit()

    user = User(username="marcola", password="123", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/auth/login", json={"username": user.username, "password": user.password}
    )

    return response.json["access_token"]


@pytest.fixture()
def create_post_test():
    post = Post(
        title="titulo teste",
        body="livro muito bom",
        created=datetime.strptime("2025-01-17T12:00:00", "%Y-%m-%dT%H:%M:%S"),
        author_id=1,
    )
    db.session.add(post)
    db.session.commit()

    return post


@pytest.fixture()
def create_role_test():
    role = Role(name="Teste")

    db.session.add(role)
    db.session.commit()

    user = User(username="teste", password="321", role_id=role.id)
    db.session.add(user)
    db.session.commit()
    return role


@pytest.fixture()
def create_role_normal():
    role = Role(name="Normal")
    db.session.add(role)
    db.session.commit()

    return role
