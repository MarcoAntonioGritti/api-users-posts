from http import HTTPStatus

from sqlalchemy import func, inspect

from apirestfull_curso.src.models import Role, User, db
from apirestfull_curso.src.views.user import UserSchema
from apirestfull_curso.src.app import bcrypt


def test_get_user_success_admin(client, access_token_admin):
    user = db.session.execute(db.select(User).where(User.id == 1)).scalar()
    user_id = user.id

    response = client.get(
        f"/users/get/{user_id}",
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )
    users_schema = UserSchema()
    user_data = users_schema.dump(user)

    assert response.status_code == HTTPStatus.OK
    assert response.json == user_data


def test_get_user_not_found(client, access_token_admin):
    invalid_user = -1

    response = client.get(
        f"/users/get/{invalid_user}",
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_list_users_success_admin(client, access_token_admin):

    role = db.session.execute(db.select(Role).where(Role.name == "Admin")).scalar()
    role_id = role.id

    user = User(username="test", password="teste123", role_id=role_id)
    db.session.add(user)
    db.session.commit()

    response = client.get(
        "/users/list", headers={"Authorization": f"Bearer {access_token_admin}"}
    )

    users = db.session.execute(db.select(User)).scalars()

    users_schema = UserSchema(many=True)
    list_user = users_schema.dump(users)

    assert response.status_code == HTTPStatus.OK
    assert response.json == list_user


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
    assert db.session.execute(db.select(func.count(User.id))).scalar() == 3


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

    data = {
        "username": "user2",
        "password": "123",
        "role_id": role_id,
    }

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
