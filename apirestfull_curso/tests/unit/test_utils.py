from http import HTTPStatus

from flask import Flask

from apirestfull_curso.src.utils import requires_roles


def test_create_app(app):
    # Vefificando se a app dada, retorna um instância do Flask
    assert isinstance(app, Flask)

    # Verificando se configurações de ambiente estão corretas
    assert app.config["SECRET_KEY"] == "test"
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite://"
    assert app.config["JWT_SECRET_KEY"] == "test"

    # Verificando se os bluenprints, estão registrados na minha aplicação
    assert "user" in app.blueprints
    assert "post" in app.blueprints
    assert "auth" in app.blueprints
    assert "role" in app.blueprints


def test_requires_roles_success(mocker):
    # Given
    mock_user = mocker.Mock()  # Um objeto aleatório que não existe
    mock_user.role.name = "admin"  # Apartir do objeto aleatório, eu posso chamar qualquer atributo(no caso role.name)
    mocker.patch("apirestfull_curso.src.utils.get_jwt_identity"),
    mocker.patch(
        "apirestfull_curso.src.utils.db.get_or_404", return_value=mock_user
    ),  # Fará uma consulta falsa e retornara o mock criado('normal')
    decorated_fuction = requires_roles("admin")(
        lambda: "success"
    )  # só será retornado success, caso a role passada e encontrada for normal,caso contrário o teste retorna um 'FAILED'

    # When
    result = decorated_fuction()

    # Then
    assert (
        result == "success"
    )  # se o resultado devolvido for 'success', então o teste deu certo


def test_requires_roles_fail(mocker):
    mock_user = mocker.Mock()  # Um objeto aleatório que não existe
    mock_user.role.name = "normal"  # Apartir do objeto aleatório, eu posso chamar qualquer atributo(no caso role.name)

    mocker.patch("apirestfull_curso.src.utils.get_jwt_identity"),
    mocker.patch("apirestfull_curso.src.utils.db.get_or_404", return_value=mock_user)

    decorated_fuction = requires_roles("admin")(lambda: "success")
    result = decorated_fuction()

    assert result == (
        {"message": "User dont have access."},
        HTTPStatus.FORBIDDEN,
    )
