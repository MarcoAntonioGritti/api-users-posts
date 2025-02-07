import pytest

from apirestfull_curso.src.app import create_app
from apirestfull_curso.src.models.base import db


@pytest.fixture()
def app():
    app = create_app(
        {
            "SECRET_KEY": "test",
            "SQLALCHEMY_DATABASE_URI": "sqlite://",  # Configurando um banco de dados em memória
            "JWT_SECRET_KEY": "test",
        }
    )
    with app.app_context():
        db.create_all()  # Cria todas as tabelas no banco de dados conforme os modelos definidos
        yield app
