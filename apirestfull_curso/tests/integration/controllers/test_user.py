from http import HTTPStatus

from sqlalchemy import func, inspect

from apirestfull_curso.src.models.base import db
from apirestfull_curso.src.models.role import Role
from apirestfull_curso.src.models.user import User


def test_get_user_success_admin(client, access_token_admin):
    user = db.session.execute(db.select(User).where(User.id == 1)).scalar()

    response = client.get(
        f"/users/get/{user.id}",
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": user.id,
        "username": user.username,
        "password": user.password,
        "role": {
            "id": user.role.id,
            "name": user.role.name,
        },
    }


def test_get_user_success_normal(client, access_token_normal):
    user = db.session.execute(db.select(User).where(User.id == 1)).scalar()

    response = client.get(
        f"/users/get/{user.id}",
        headers={"Authorization": f"Bearer {access_token_normal}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": user.id,
        "username": user.username,
        "password": user.password,
        "role": {
            "id": user.role.id,
            "name": user.role.name,
        },
    }


def test_get_user_not_found(client, access_token_admin):
    invalid_user = -1

    response = client.get(
        f"/users/get/{invalid_user}",
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_list_users_success_admin(client):

    role = Role(name="Admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="marcola", password="123", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/auth/login", json={"username": user.username, "password": user.password}
    )

    access_token = response.json["access_token"]

    response = client.get(
        "/users/list", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == [
        {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "role": {
                "id": user.role.id,
                "name": user.role.name,
            },
        }
    ]


def test_list_users_success_normal(client):
    role_normal = Role(name="Normal")
    db.session.add(role_normal)
    db.session.commit()

    user = User(username="marcola", password="123", role_id=role_normal.id)
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/auth/login", json={"username": user.username, "password": user.password}
    )

    access_token = response.json["access_token"]

    response = client.get(
        "/users/list", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == [
        {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "role": {
                "id": user.role.id,
                "name": user.role.name,
            },
        }
    ]


def test_create_user(client, access_token_admin):
    role_id = db.session.execute(
        db.select(Role.id).where(Role.name == "Admin")
    ).scalar()
    payload = {"username": "user2", "password": "user2", "role_id": role_id}

    response = client.post(
        f"/users/created",
        json=payload,
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "User created!"}
    assert db.session.execute(db.select(func.count(User.id))).scalar() == 2


def test_create_user_forbidden(client, access_token_normal):
    role_id = db.session.execute(
        db.select(Role.id).where(Role.name == "Normal")
    ).scalar()
    payload = {"username": "user2", "password": "user2", "role_id": role_id}

    response = client.post(
        f"/users/created",
        json=payload,
        headers={"Authorization": f"Bearer {access_token_normal}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json == {"message": "User dont have access."}


def test_update_users_success(client, access_token_admin):
    user = db.session.execute(db.select(User).where(User.id == 1)).scalar()
    role_id = db.session.execute(
        db.select(Role.id).where(Role.name == "Admin")
    ).scalar()

    data = {"username": "user2", "password": "user2", "role_id": role_id}

    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])

    db.session.commit()

    response = client.patch(
        f"/users/update/{user.id}",
        json=data,
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": user.id,
        "username": user.username,
        "password": user.password,
        "role_id": user.role_id,
    }


def test_update_users_forbidden(client, access_token_normal):
    user = db.session.execute(db.select(User).where(User.id == 1)).scalar()
    role_id = db.session.execute(
        db.select(Role.id).where(Role.name == "Normal")
    ).scalar()

    data = {"username": "user2", "password": "user2", "role_id": role_id}

    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])

    db.session.commit()

    response = client.patch(
        f"/users/update/{user.id}",
        json=data,
        headers={"Authorization": f"Bearer {access_token_normal}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json == {"message": "User dont have access."}


def test_update_users_not_found(client, access_token_admin):
    invalid_user = -1

    role_id = db.session.execute(
        db.select(Role.id).where(Role.name == "Admin")
    ).scalar()

    data = {"username": "user2", "password": "user2", "role_id": role_id}

    response = client.patch(
        f"/users/update/{invalid_user}",
        json=data,
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_success(client, access_token_admin):
    user = db.session.execute(db.select(User).where(User.id == 1)).scalar()
    response = client.delete(
        f"/users/delete/{user.id}",
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT

    user_in_db = db.session.execute(db.select(User).where(User.id == 1)).scalar()

    assert user_in_db is None


def test_user_delete_forbidden(client, access_token_normal):
    user = db.session.execute(db.select(User).where(User.id == 1)).scalar()
    response = client.delete(
        f"/users/delete/{user.id}",
        headers={"Authorization": f"Bearer {access_token_normal}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_user_delete_not_found(client, access_token_admin):

    invalid_user = -1

    response = client.delete(
        f"/users/delete/{invalid_user}",
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
