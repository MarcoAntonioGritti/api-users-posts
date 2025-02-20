from http import HTTPStatus

from apirestfull_curso.src.models.base import db
from apirestfull_curso.src.models.role import Role
from apirestfull_curso.src.models.user import User


def test_get_role_success_admin(client, create_role_test, access_token_admin):
    role = create_role_test

    role_get_id = role.id

    response = client.get(
        f"/roles/get/{role_get_id}",
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": role.id,
        "name": role.name,
        "users": [{"id": user.id, "username": user.username} for user in role.users],
    }


def test_get_role_success_normal(client, create_role_test, access_token_normal):
    role = create_role_test

    role_get_id = role.id

    response = client.get(
        f"/roles/get/{role_get_id}",
        headers={"Authorization": f"Bearer {access_token_normal}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json == {"message": "User dont have access."}


def test_get_role_not_found(client, access_token_admin):
    invalid_role = -1

    response = client.get(
        f"/roles/get/{invalid_role}",
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_list_roles_access_admin(client, access_token_admin):

    role = Role(name="Teste")

    db.session.add(role)
    db.session.commit()

    user = User(username="teste", password="321", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.get(
        "/roles/list",
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    new_role_data = {
        "id": role.id,
        "name": role.name,
        "user": [user.username],
    }

    assert response.status_code == HTTPStatus.OK
    assert new_role_data in response.json


def test_list_roles__access_forbidden(client, access_token_normal):
    role = Role(name="Teste")

    db.session.add(role)
    db.session.commit()

    user = User(username="teste", password="321", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.get(
        "/roles/list",
        headers={"Authorization": f"Bearer {access_token_normal}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json == {"message": "User dont have access."}


def test_create_role_success(client, access_token_admin):
    data = {"name": "Teste"}

    response = client.post(
        "/roles/created",
        json=data,
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "Role created!"}


def test_create_role_forbidden(client, access_token_normal):
    data = {"name": "Teste"}

    response = client.post(
        "/roles/created",
        json=data,
        headers={"Authorization": f"Bearer {access_token_normal}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_role_success(client, access_token_admin):

    role = Role(name="Teste")

    db.session.add(role)
    db.session.commit()

    user = User(username="teste", password="321", role_id=role.id)
    db.session.add(user)
    db.session.commit()
    # Verificar que o papel e o usuário foram criados
    assert role.id is not None
    assert user.id is not None

    # Remover o usuário associado antes de deletar o papel
    db.session.delete(user)
    db.session.commit()

    # Deletar o papel
    response = client.delete(
        f"/roles/delete/{role.id}",
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_role_forbidden(client, access_token_normal):
    role = Role(name="Teste")
    db.session.add(role)
    db.session.commit()
    user = User(username="teste", password="321", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    assert role.id is not None
    assert user.id is not None

    db.session.delete(user)
    db.session.commit()

    response = client.delete(
        f"/roles/delete/{role.id}",
        headers={"Authorization": f"Bearer {access_token_normal}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json == {"message": "User dont have access."}


def test_delete_role_not_found(client, access_token_normal):
    invalid_role = -1
    user = User(username="teste", password="321", role_id=invalid_role)
    db.session.add(user)
    db.session.commit()

    assert user.id is not None

    db.session.delete(user)
    db.session.commit()

    response = client.delete(
        f"/roles/delete/{invalid_role}",
        headers={"Authorization": f"Bearer {access_token_normal}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
