from datetime import datetime

import pytest

from apirestfull_curso.src.app import create_app
from apirestfull_curso.src.models.base import db
from apirestfull_curso.src.models.post import Post
from apirestfull_curso.src.models.role import Role
from apirestfull_curso.src.models.user import User
from apirestfull_curso.src.app import bcrypt


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
    # Busca a role "Admin"
    role = db.session.execute(db.select(Role).where(Role.name == "Admin")).scalar()
    role_id = role.id

    # Cria um usuário admin
    user = User(
        username="marcola",
        password=bcrypt.generate_password_hash("123"),  # Senha criptografada
        role_id=role_id,
    )
    db.session.add(user)
    db.session.commit()  # Confirma a transação

    # Faz login com o usuário criado
    response = client.post(
        "/auth/login",
        json={"username": user.username, "password": "123"},  # Senha em texto plano
    )

    data = response.json
    return data["access_token"]  # Retorna o token de acesso


@pytest.fixture()
def access_token_normal(client):
    role = Role(name="Normal")
    db.session.add(role)
    db.session.commit()

    user = User(
        username="marcola",
        password=bcrypt.generate_password_hash("123"),
        role_id=role.id,
    )
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/auth/login", json={"username": user.username, "password": "123"}
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


@pytest.fixture()
def create_user_test():
    role = Role(name="Normal")
    db.session.add(role)
    db.session.commit()

    user = User(
        username="marcola",
        password=bcrypt.generate_password_hash("123"),
        role_id=role.id,
    )
    db.session.add(user)
    db.session.commit()

    return user
