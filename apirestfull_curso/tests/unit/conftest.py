import pytest

from apirestfull_curso.src.app import create_app
from apirestfull_curso.src.models.base import db


@pytest.fixture()
def app():
    # Cria a aplicação (usará o ambiente definido pela variável de ambiente)
    app = create_app("testing")

    # Entra no contexto da aplicação
    with app.app_context():
        db.create_all()  # Cria todas as tabelas no banco de dados
        yield app  # Retorna a aplicação para o teste
